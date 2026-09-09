#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -x ".venv/bin/python" ]; then
    echo "Nicht installiert. Bitte zuerst ausfuehren: ./install.sh"
    exit 1
fi

./.venv/bin/python main.py
