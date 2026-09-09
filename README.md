# Live Flaechen-Effekt

Live-Kameraeffekt per Handverfolgung: beide Haende zeigen, Daumen+Zeigefinger
spannen eine Flaeche auf dem Kamerabild auf, darin erscheint ein Effekt.
Optional als virtuelle Kamera fuer OBS/Zoom/Discord nutzbar.

## Voraussetzungen

- Linux mit Webcam
- Python 3.10, 3.11 oder 3.12 (MediaPipe unterstuetzt aktuell keine neueren
  Versionen zuverlaessig)

## Installation

    ./install.sh

Legt ein lokales `.venv` an und installiert alle Abhaengigkeiten dort hinein.
Veraendert nichts systemweit (ausser du richtest v4l2loopback ein, siehe unten).

## Starten

    ./run.sh

Es oeffnet sich ein Vorschaufenster mit Kamerabild + Sidebar rechts.

## Virtuelle Kamera fuer OBS/Zoom/Discord (optional)

    sudo apt install v4l2loopback-dkms
    sudo modprobe v4l2loopback devices=1 exclusive_caps=1 card_label="Live Effekt Cam"

Ohne das laeuft die App trotzdem, nur ohne Streaming-Ausgabe (nur das lokale
Vorschaufenster). Der Streaming-Ausgang zeigt nie Sidebar/Umriss/Text, nur
Kamera + Effekt.

## Bedienung

- Beide Haende zeigen (offene Hand), Daumen+Zeigefinger spannen eine Flaeche
  auf -> Effekt erscheint darin
- Sidebar rechts: Effekt per Mausklick waehlen
- Tasten `0`-`9`, `p`, `h`, `n`: Effekt direkt waehlen (Liste in der Sidebar)
- Eine Hand kurz zusammenkneifen (Daumen+Zeigefinger) = Effekt zufaellig
  wechseln
- Rechte Hand: Daumen+Mittelfinger zusammen = aktuelle Flaeche einfrieren
  (bleibt an Ort stehen)
- Linke Hand: Daumen+Mittelfinger zusammen = alle eingefrorenen Flaechen
  entfernen
- `r` = Effekt manuell zufaellig wechseln, `q`/`Esc` = beenden

## Problembehebung

- **Kamera oeffnet nicht**: pruefen ob ein anderes Programm sie gerade nutzt,
  ggf. `CAMERA_INDEX` in `src/config.py` anpassen (mehrere Kameras -> anderer
  Index als 0).
- **Handverfolgung reagiert nicht**: gute Beleuchtung hilft, Hand komplett im
  Bild halten.
- **Keine virtuelle Kamera verfuegbar**: siehe Abschnitt oben, v4l2loopback
  muss geladen sein bevor die App startet.
