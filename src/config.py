import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAND_MODEL_PATH = os.path.join(BASE_DIR, "hand_landmarker.task")

CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
TARGET_FPS = 30

# Fläche (Viereck aus Daumen+Zeigefinger beider Hände)
QUAD_MASK_FEATHER = 25  # Weichzeichnung der Flächen-Kante (Pixel, ungerade empfohlen)
WARP_RIPPLE_RADIUS = 100  # Wirkungsradius der Warp-Ripple je Eckpunkt

FINGERTIP_EMA_ALPHA = 0.5  # Glättung der Fingerspitzen-Position (0..1, höher = reaktiver)

# Pinch-Gesten
PINCH_DISTANCE_RATIO = 0.35  # Pinch-Distanz / Handgröße (Handgelenk-Mittelfinger-Basis)
GESTURE_COOLDOWN_FRAMES = 20  # Sperrzeit nach Auslösen einer Pinch-Geste, verhindert Mehrfach-Trigger
# Daumen+Zeigefinger (egal welche Hand)         -> zufälliger Effektwechsel
# Daumen+Mittelfinger rechte Hand                -> aktuelle Fläche+Effekt einfrieren
# Daumen+Mittelfinger linke Hand                 -> alle eingefrorenen Flächen entfernen
MAX_FROZEN_ZONES = 8  # älteste eingefrorene Fläche fliegt raus, wenn mehr angelegt werden

# Keybindings -> effect names ("off" = kein Effekt)
KEY_EFFECT_MAP = {
    ord("0"): "off",
    ord("1"): "glitch",
    ord("2"): "warp",
    ord("3"): "combo",
    ord("4"): "grayscale",
    ord("5"): "invert",
    ord("6"): "darken",
    ord("7"): "pixelate",
    ord("8"): "edge",
    ord("9"): "thermal",
    ord("p"): "posterize",
    ord("h"): "huecycle",
    ord("n"): "staticnoise",
}
KEY_RANDOMIZE = ord("r")  # manueller Zufalls-Trigger zum Testen, ohne Geste
KEY_QUIT = {ord("q"), 27}  # 27 = Esc

DEFAULT_EFFECT = "combo"

WINDOW_NAME = "Live Flaechen-Effekt"
