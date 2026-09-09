#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_BIN=""
for cand in python3.10 python3.11 python3.12 python3; do
    if command -v "$cand" >/dev/null 2>&1; then
        PYTHON_BIN="$cand"
        break
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    echo "Kein Python 3 gefunden. Bitte Python 3.10, 3.11 oder 3.12 installieren"
    echo "(z.B. 'sudo apt install python3.10 python3.10-venv')."
    exit 1
fi

echo "Nutze $PYTHON_BIN ($($PYTHON_BIN --version 2>&1))"
echo ""

"$PYTHON_BIN" -m venv .venv
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

chmod +x run.sh

echo ""
echo "Fertig installiert. Starten mit: ./run.sh"
echo ""
echo "Fuer die virtuelle Kamera (Streaming in OBS/Zoom/Discord) wird das"
echo "Kernel-Modul v4l2loopback benoetigt:"
echo "    sudo apt install v4l2loopback-dkms"
echo "    sudo modprobe v4l2loopback devices=1 exclusive_caps=1 card_label=\"Live Effekt Cam\""
echo "Ohne das laeuft die App trotzdem, nur ohne Streaming-Ausgabe (nur Vorschaufenster)."
