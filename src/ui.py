from typing import Dict, Optional, Tuple

import cv2
import numpy as np

from .effects import EFFECTS

SIDEBAR_WIDTH = 220

_BG_COLOR = (25, 25, 25)
_BUTTON_COLOR = (55, 55, 55)
_BUTTON_ACTIVE_COLOR = (0, 200, 255)
_TEXT_COLOR = (230, 230, 230)
_TEXT_ACTIVE_COLOR = (10, 10, 10)
_MUTED_TEXT_COLOR = (150, 150, 150)

_BUTTON_HEIGHT = 32
_BUTTON_GAP = 6
_BUTTON_MARGIN_X = 12
_BUTTON_START_Y = 66

EFFECT_NAMES = list(EFFECTS.keys())  # inkl. "off", feste Reihenfolge fürs Layout


def button_rects() -> Dict[str, Tuple[int, int, int, int]]:
    """Liefert {effekt_name: (x0, y0, x1, y1)} in Sidebar-lokalen Koordinaten."""
    rects = {}
    y = _BUTTON_START_Y
    for name in EFFECT_NAMES:
        x0, x1 = _BUTTON_MARGIN_X, SIDEBAR_WIDTH - _BUTTON_MARGIN_X
        y1 = y + _BUTTON_HEIGHT
        rects[name] = (x0, y, x1, y1)
        y = y1 + _BUTTON_GAP
    return rects


def build_sidebar(
    height: int, current_effect: str, hands_visible: int, vcam_active: bool, frozen_count: int = 0
) -> np.ndarray:
    """Steuerungs-Panel (Effekt-Liste, Status). Nur für die lokale Vorschau gedacht,
    wird nie in den Kamera-/Stream-Output eingemischt."""
    sidebar = np.full((height, SIDEBAR_WIDTH, 3), _BG_COLOR, dtype=np.uint8)

    cv2.putText(sidebar, "STEUERUNG", (14, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, _TEXT_COLOR, 1, cv2.LINE_AA)
    cv2.line(sidebar, (12, 42), (SIDEBAR_WIDTH - 12, 42), (80, 80, 80), 1)

    rects = button_rects()
    for name, (x0, y0, x1, y1) in rects.items():
        active = name == current_effect
        color = _BUTTON_ACTIVE_COLOR if active else _BUTTON_COLOR
        text_color = _TEXT_ACTIVE_COLOR if active else _TEXT_COLOR
        cv2.rectangle(sidebar, (x0, y0), (x1, y1), color, -1, cv2.LINE_AA)
        cv2.putText(
            sidebar, name, (x0 + 10, y0 + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.48, text_color, 1, cv2.LINE_AA
        )

    status_y = list(rects.values())[-1][3] + 30
    cv2.line(sidebar, (12, status_y - 16), (SIDEBAR_WIDTH - 12, status_y - 16), (80, 80, 80), 1)
    cv2.putText(
        sidebar, f"Haende: {hands_visible}/2", (14, status_y + 6),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, _TEXT_COLOR, 1, cv2.LINE_AA,
    )
    cv2.putText(
        sidebar, f"Virtual Cam: {'an' if vcam_active else 'aus'}", (14, status_y + 28),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, _TEXT_COLOR, 1, cv2.LINE_AA,
    )
    cv2.putText(
        sidebar, f"Eingefroren: {frozen_count}", (14, status_y + 50),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, _TEXT_COLOR, 1, cv2.LINE_AA,
    )
    cv2.putText(
        sidebar, "re. Daumen+Mittelf. = einfrieren", (14, status_y + 74),
        cv2.FONT_HERSHEY_SIMPLEX, 0.4, _MUTED_TEXT_COLOR, 1, cv2.LINE_AA,
    )
    cv2.putText(
        sidebar, "li. Daumen+Mittelf. = loeschen", (14, status_y + 94),
        cv2.FONT_HERSHEY_SIMPLEX, 0.4, _MUTED_TEXT_COLOR, 1, cv2.LINE_AA,
    )
    cv2.putText(
        sidebar, "r = zufaellig, q = beenden", (14, status_y + 118),
        cv2.FONT_HERSHEY_SIMPLEX, 0.4, _MUTED_TEXT_COLOR, 1, cv2.LINE_AA,
    )

    return sidebar


def hit_test(local_x: int, local_y: int) -> Optional[str]:
    """local_x/local_y bereits relativ zur Sidebar (0 = linke Sidebar-Kante).
    Gibt den angeklickten Effekt-Namen zurück, oder None."""
    for name, (x0, y0, x1, y1) in button_rects().items():
        if x0 <= local_x <= x1 and y0 <= local_y <= y1:
            return name
    return None
