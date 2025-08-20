#!/usr/bin/env bash
set -euo pipefail

echo ">>> Removing old installs..."
python -m pip uninstall -y prefiq || true
python -m pip cache purge || true

echo ">>> Installing local project..."
python -m pip install .

echo ">>> Verifying CLI..."
prefiq --help
echo
prefiq doctor boot || true
