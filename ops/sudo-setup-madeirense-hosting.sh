#!/usr/bin/env bash
#
# One-time root setup to publish the Elucidário Madeirense at https://madeirense.geocube.work
#
#   sudo bash ops/sudo-setup-madeirense-hosting.sh            # behind the shared basic auth (default)
#   sudo bash ops/sudo-setup-madeirense-hosting.sh --public   # no auth
#
# Same shape as the other published sites on this host (see /etc/caddy/Caddyfile):
#  - webroot /srv/sites/madeirense/www, owned by dimi, so publishing never needs root again
#    (Caddy runs as `caddy` and cannot traverse /home/dimi);
#  - a Caddy vhost on the shared loopback 127.0.0.1:8080, `http://` because TLS ends at Cloudflare;
#  - a cloudflared ingress rule inserted ABOVE the http_status:404 catch-all.
# The DNS CNAME was created separately as dimi (`cloudflared tunnel route dns infinity madeirense.geocube.work`).
# Both config files are backed up and validated on a copy before being installed.

set -euo pipefail

SITE="madeirense"
HOST="madeirense.geocube.work"
OWNER="dimi"
WWW="/srv/sites/$SITE/www"
CADDYFILE="/etc/caddy/Caddyfile"
CF_CONFIG="/etc/cloudflared/config.yml"
STAMP="$(date +%Y%m%d-%H%M%S)"
AUTH_LINE="	import auth"
[[ "${1:-}" == "--public" ]] && AUTH_LINE="	# public: no basic auth"

[[ $EUID -eq 0 ]] || { echo "Run me with sudo." >&2; exit 1; }
log() { printf '==> %s\n' "$*"; }
die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

# ---------------------------------------------------------------- 1. webroot
log "Creating $WWW (owner $OWNER)"
install -d -o "$OWNER" -g "$OWNER" -m 755 /srv/sites "/srv/sites/$SITE" "$WWW"
if [[ ! -e "$WWW/index.html" ]]; then
  printf '<!doctype html><meta charset="utf-8"><title>Elucidário Madeirense</title><p>Hosting is up. The site has not been published yet.</p>\n' > "$WWW/index.html"
  chown "$OWNER:$OWNER" "$WWW/index.html"
fi

# ---------------------------------------------------------------- 2. Caddy
if grep -q "$HOST" "$CADDYFILE"; then
  log "Caddyfile already has a $HOST block — leaving it alone"
else
  log "Backing up $CADDYFILE -> $CADDYFILE.bak-$STAMP"
  cp -a "$CADDYFILE" "$CADDYFILE.bak-$STAMP"
  TMP_CADDY="$(mktemp)"
  cp "$CADDYFILE" "$TMP_CADDY"
  cat >> "$TMP_CADDY" <<EOF

# Elucidário Madeirense — static Astro site (~30 k pages, 4 languages), published to $WWW
# by ops/publish-site.sh in the elucidario_madeirense repo. Loopback-only on the shared 8080,
# explicit http:// (TLS ends at Cloudflare).
http://$HOST:8080 {
	bind 127.0.0.1 ::1
$AUTH_LINE
	root * $WWW

	encode gzip zstd

	# Content-hashed bundles and search indexes never change under the same name.
	@immutable path /_astro/* /search/*/corpus.* /search/*/suggest-*
	header @immutable Cache-Control "public, max-age=31536000, immutable"
	@fonts path *.woff2
	header @fonts Cache-Control "public, max-age=31536000, immutable"

	file_server

	handle_errors {
		@notfound expression {err.status_code} == 404
		rewrite @notfound /404.html
		file_server
	}
}
EOF
  log "Validating the proposed Caddyfile"
  caddy validate --config "$TMP_CADDY" --adapter caddyfile
  install -o root -g root -m 644 "$TMP_CADDY" "$CADDYFILE"
  rm -f "$TMP_CADDY"
fi

# Restart, not reload: the Caddyfile has `admin off`, so `caddy reload` cannot reach the admin API.
log "Restarting caddy"
systemctl restart caddy
for attempt in 1 2 3 4 5; do
  sleep 1
  CODE="$(curl -sS -o /dev/null -w '%{http_code}' -H "Host: $HOST" http://127.0.0.1:8080/ || echo 000)"
  case "$CODE" in
    401|200|404) log "    caddy is serving $HOST (HTTP $CODE)"; break ;;
    *) [[ $attempt -eq 5 ]] && die "caddy restarted but $HOST answers $CODE — check: journalctl -u caddy -n 50" ;;
  esac
done

# ---------------------------------------------------------------- 3. tunnel
if grep -q "$HOST" "$CF_CONFIG"; then
  log "cloudflared config already has $HOST — leaving it alone"
else
  log "Backing up $CF_CONFIG -> $CF_CONFIG.bak-$STAMP"
  cp -a "$CF_CONFIG" "$CF_CONFIG.bak-$STAMP"
  TMP_CF="$(mktemp)"
  awk -v host="$HOST" '
    !done && /http_status:404/ {
      print "  - hostname: " host
      print "    service: http://localhost:8080"
      done = 1
    }
    { print }
  ' "$CF_CONFIG" > "$TMP_CF"
  grep -q "$HOST" "$TMP_CF" || { rm -f "$TMP_CF"; die "no http_status:404 catch-all found in $CF_CONFIG; add the rule by hand above it"; }

  # Validate differentially: the installed config already carries options this cloudflared warns about.
  BASE_OK=0
  cloudflared --config "$CF_CONFIG" tunnel ingress validate >/dev/null 2>&1 && BASE_OK=1
  if ! cloudflared --config "$TMP_CF" tunnel ingress validate; then
    (( BASE_OK )) && { rm -f "$TMP_CF"; die "the edit broke the ingress config. Nothing installed."; }
    log "    (the existing config already fails validation; unchanged by us, continuing)"
  fi
  cloudflared --config "$TMP_CF" tunnel ingress rule "https://$HOST/"
  install -o root -g root -m 644 "$TMP_CF" "$CF_CONFIG"
  rm -f "$TMP_CF"
  log "Restarting cloudflared"
  systemctl restart cloudflared
fi

cat <<EOF

==> Root setup done. Publish (as dimi, no sudo):

  ops/publish-site.sh

Then open https://$HOST/
EOF
