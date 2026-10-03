#!/usr/bin/env bash
#
# Build the website and publish it to https://madeirense.geocube.work (served by Caddy from /srv/sites/madeirense/www).
#
#   ops/publish-site.sh             # export data if missing, build, publish
#   ops/publish-site.sh --export    # also regenerate site/data from the pipeline first
#
# Runs as dimi; no root. One-time root setup: sudo bash ops/sudo-setup-madeirense-hosting.sh
#
# The build goes to a staging directory, never straight into the webroot, so a failed build leaves the live site
# untouched. rsync --delay-updates then swaps the files in at the end of the transfer.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WWW="/srv/sites/madeirense/www"
STAGE="${XDG_CACHE_HOME:-$HOME/.cache}/madeirense-build"
URL="https://madeirense.geocube.work/"

log() { printf '==> %s\n' "$*"; }
die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

[[ -d "$WWW" && -w "$WWW" ]] || die "$WWW missing or not writable — run: sudo bash ops/sudo-setup-madeirense-hosting.sh"

if [[ "${1:-}" == "--export" || ! -f "$REPO/site/data/meta.json" ]]; then
  log "Exporting site data (site_export)"
  (cd "$REPO" && uv run python -c "from elucidario.stages import site_export as S; S.run()")
fi

log "Building search indexes and site into $STAGE"
cd "$REPO/site"
[[ -d node_modules ]] || npm ci
node scripts/build-search.mjs
rm -rf "$STAGE"
npx astro build --outDir "$STAGE"
[[ -f "$STAGE/index.html" && -f "$STAGE/en/index.html" ]] || die "build output looks incomplete; not publishing"
# Review-only artefacts that live in public/ but should not be published.
rm -f "$STAGE/art/gallery.html" "$STAGE"/art/og-*.svg "$STAGE"/art/og-*.png "$STAGE/maps/demo.html"

log "Publishing to $WWW"
rsync -a --delete --delay-updates "$STAGE/" "$WWW/"

read -r CODE BYTES < <(curl -sS -o /dev/null -w '%{http_code} %{size_download}\n' -H "Host: madeirense.geocube.work" http://127.0.0.1:8080/en/ || echo "000 0")
if [[ "$CODE" == 401 ]]; then log "Local check: served behind basic auth (HTTP 401)"
elif [[ "$CODE" == 200 && "$BYTES" -gt 0 ]]; then log "Local check: served publicly (HTTP 200, $BYTES bytes)"
else log "Local check: Caddy has no vhost for the site yet (HTTP $CODE, $BYTES bytes) — run: sudo bash ops/sudo-setup-madeirense-hosting.sh"; fi
log "Done: $URL"
