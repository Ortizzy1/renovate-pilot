#!/usr/bin/env bash
# Fails if either lockfile is out of sync with its manifest. Mutates nothing tracked.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"

echo "== npm: lockfile vs package.json"
cd "$root/npm-app"
npm ci --dry-run --ignore-scripts --no-audit --no-fund >/dev/null
tmp="$(mktemp -d)"; cp package.json package-lock.json "$tmp/"
( cd "$tmp" && npm install --package-lock-only --ignore-scripts --no-audit --no-fund >/dev/null )
diff -q package-lock.json "$tmp/package-lock.json" >/dev/null || { echo "package-lock.json is stale"; exit 1; }
rm -rf "$tmp"

echo "== uv: lockfile vs pyproject.toml"
cd "$root/py-app"
uv lock --check
echo "lockfiles consistent"
