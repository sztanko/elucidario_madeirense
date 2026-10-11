#!/usr/bin/env bash
#
# One-time root setup: serve the Elucidário Madeirense at https://elucidariomadeirense.pt (the primary address from now
# on), with www.elucidariomadeirense.pt and the old https://madeirense.geocube.work answering 301 to it.
#
#   sudo bash ops/sudo-add-domain-elucidariomadeirense.sh                # .pt primary, others redirect (default)
#   sudo bash ops/sudo-add-domain-elucidariomadeirense.sh --no-redirect  # serve the site on all three names
#
# Run it only AFTER the zone elucidariomadeirense.pt is active in Cloudflare and its two DNS records point at the
# tunnel (CNAME @ and www -> <tunnel id>.cfargotunnel.com, proxied) — otherwise the redirect would send visitors to
# a name that does not resolve yet.
# Same shape as ops/sudo-setup-madeirense-hosting.sh: Caddy on the shared loopback 127.0.0.1:8080 (TLS ends at
# Cloudflare), cloudflared ingress rules above the http_status:404 catch-all; both files backed up and validated on a
# copy before being installed. Idempotent.

set -euo pipefail

NEW="elucidariomadeirense.pt"
WWW_NEW="www.elucidariomadeirense.pt"
OLD="madeirense.geocube.work"
CADDYFILE="/etc/caddy/Caddyfile"
CF_CONFIG="/etc/cloudflared/config.yml"
STAMP="$(date +%Y%m%d-%H%M%S)"
REDIRECT=1
[[ "${1:-}" == "--no-redirect" ]] && REDIRECT=0

[[ $EUID -eq 0 ]] || { echo "Run me with sudo." >&2; exit 1; }
log() { printf '==> %s\n' "$*"; }
die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

# ---------------------------------------------------------------- 1. Caddy
if grep -q "http://$NEW:8080" "$CADDYFILE"; then
  log "Caddyfile already serves $NEW — leaving it alone"
else
  grep -q "^http://$OLD:8080 {" "$CADDYFILE" || die "no 'http://$OLD:8080 {' block in $CADDYFILE"
  log "Backing up $CADDYFILE -> $CADDYFILE.bak-$STAMP"
  cp -a "$CADDYFILE" "$CADDYFILE.bak-$STAMP"
  TMP_CADDY="$(mktemp)"
  if (( REDIRECT )); then
    # the site block now answers for the .pt apex; www and the old subdomain get a permanent redirect
    sed "s|^http://$OLD:8080 {|http://$NEW:8080 {|" "$CADDYFILE" > "$TMP_CADDY"
    cat >> "$TMP_CADDY" <<EOF

# Elucidário Madeirense — old and www names redirect to the primary address https://$NEW
http://$WWW_NEW:8080, http://$OLD:8080 {
	bind 127.0.0.1 ::1
	redir https://$NEW{uri} permanent
}
EOF
  else
    sed "s|^http://$OLD:8080 {|http://$OLD:8080, http://$NEW:8080, http://$WWW_NEW:8080 {|" "$CADDYFILE" > "$TMP_CADDY"
  fi
  log "Validating the proposed Caddyfile"
  caddy validate --config "$TMP_CADDY" --adapter caddyfile
  install -o root -g root -m 644 "$TMP_CADDY" "$CADDYFILE"
  rm -f "$TMP_CADDY"
  # Restart, not reload: the Caddyfile has `admin off`.
  log "Restarting caddy"
  systemctl restart caddy
fi
for attempt in 1 2 3 4 5; do
  sleep 1
  CODE="$(curl -sS -o /dev/null -w '%{http_code}' -H "Host: $NEW" http://127.0.0.1:8080/en/ || echo 000)"
  [[ "$CODE" == 200 ]] && { log "    caddy is serving $NEW (HTTP $CODE)"; break; }
  [[ $attempt -eq 5 ]] && die "caddy answers $CODE for $NEW — check: journalctl -u caddy -n 50"
done

# ---------------------------------------------------------------- 2. tunnel
if grep -q "hostname: $NEW\$" "$CF_CONFIG"; then
  log "cloudflared config already has $NEW — leaving it alone"
else
  log "Backing up $CF_CONFIG -> $CF_CONFIG.bak-$STAMP"
  cp -a "$CF_CONFIG" "$CF_CONFIG.bak-$STAMP"
  TMP_CF="$(mktemp)"
  awk -v a="$NEW" -v b="$WWW_NEW" '
    !done && /http_status:404/ {
      print "  - hostname: " a
      print "    service: http://localhost:8080"
      print "  - hostname: " b
      print "    service: http://localhost:8080"
      done = 1
    }
    { print }
  ' "$CF_CONFIG" > "$TMP_CF"
  grep -q "$NEW" "$TMP_CF" || { rm -f "$TMP_CF"; die "no http_status:404 catch-all in $CF_CONFIG; add the rules by hand above it"; }
  BASE_OK=0
  cloudflared --config "$CF_CONFIG" tunnel ingress validate >/dev/null 2>&1 && BASE_OK=1
  if ! cloudflared --config "$TMP_CF" tunnel ingress validate; then
    (( BASE_OK )) && { rm -f "$TMP_CF"; die "the edit broke the ingress config. Nothing installed."; }
    log "    (the existing config already fails validation; unchanged by us, continuing)"
  fi
  cloudflared --config "$TMP_CF" tunnel ingress rule "https://$NEW/"
  install -o root -g root -m 644 "$TMP_CF" "$CF_CONFIG"
  rm -f "$TMP_CF"
  log "Restarting cloudflared"
  systemctl restart cloudflared
fi

cat <<EOF

==> Root setup done. Check from outside:

  curl -sI https://$NEW/en/ | head -1          # 200
  curl -sI https://$OLD/en/ | grep -i location # -> https://$NEW/en/ (unless --no-redirect)

Then switch the site's canonical address (astro.config.mjs \`site\`, ops/publish-site.sh URL/Host) and republish.
EOF
