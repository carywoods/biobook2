#!/usr/bin/env bash
# Publish the Hugo site to GitHub Pages (gh-pages branch).
#
# Usage:  ./publish.sh
#
# Requires: hugo extended >= 0.158.0 on PATH, SSH access to the repo.
set -euo pipefail

REPO_SSH="git@github.com:carywoods/biobook2.git"
BASEURL="https://carywoods.github.io/biobook2/"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "==> Building with baseURL $BASEURL"
cd "$SRC"
rm -rf public resources

# NOTE: hugo.toml sets relativeURLs=true (kept for other deploy targets).
# GitHub Pages needs absolute paths under the /biobook2/ subpath, so override it.
HUGO_RELATIVEURLS=false hugo --minify --gc --baseURL "$BASEURL"

test -f public/index.html || { echo "ERROR: no public/index.html built"; exit 1; }
touch public/.nojekyll   # stop GitHub running Jekyll on the output

PAGES=$(find public -name '*.html' | wc -l)
echo "==> Built $PAGES HTML pages"

echo "==> Pushing to gh-pages"
cp -r public "$TMP/site"
cd "$TMP/site"
git init -q -b gh-pages
git add -A
git -c user.email="cary@indybiosystems.com" -c user.name="Cary Woods" \
    commit -q -m "Publish site $(date -u '+%Y-%m-%d %H:%M UTC')"
git remote add origin "$REPO_SSH"
git push -f -q origin gh-pages

echo "==> Done. Live at $BASEURL"
echo "    (first time only: enable Pages in repo Settings -> Pages -> branch gh-pages, / root)"
