#!/usr/bin/env bash
set -euo pipefail

# Repo root = this script's directory
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PYTHON:-python}"

echo ">>> Repo root: $ROOT"
echo ">>> Python: $($PY -V)"

SITE_PKGS="$($PY - <<'PY'
import sysconfig; print(sysconfig.get_paths()['purelib'])
PY
)"
echo ">>> site-packages: $SITE_PKGS"

echo ">>> Uninstall any installed 'prefiq' and remove leftovers..."
$PY -m pip uninstall -y prefiq || true
rm -rf "$SITE_PKGS/prefiq" "$SITE_PKGS"/prefiq-*.dist-info 2>/dev/null || true

echo ">>> Clear pip cache..."
$PY -m pip cache purge || true

echo ">>> Ensure build tools..."
$PY -m pip install -U pip wheel setuptools

# Ensure config directory exists for dev
mkdir -p "$ROOT/config"
: > "$ROOT/config/apps.cfg"

# Pin project root so runtime reads THIS repo's config/apps.cfg
export PREFIQ_PROJECT_ROOT="$ROOT"
# If you use a repo .env, uncomment:
# export ENV_FILE="$ROOT/.env"

echo ">>> Editable install..."
$PY -m pip install -e "$ROOT"

echo ">>> Verify CLI:"
prefiq --help >/dev/null
prefiq app list || true
