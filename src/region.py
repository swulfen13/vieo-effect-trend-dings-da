from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np

from . import config
from .hand_tracker import HandCorners


def get_quad_points(hands: Dict[str, HandCorners]) -> Optional[List[Tuple[int, int]]]:
    """Liefert die 4 Eckpunkte in fester Umlauf-Reihenfolge (linker Daumen -> linker
    Zeigefinger -> rechter Zeigefinger -> rechter Daumen), oder None solange nicht
    beide Hände sichtbar sind. Die feste Reihenfolge (statt Neusortierung pro Frame)
    sorgt dafür, dass jede Ecke fest an ihrem Finger "klebt" und sich beim Drehen der
    Hand mitdreht, statt bei größerem Handabstand zu kippen/verdrehen."""
    left, right = hands.get("Left"), hands.get("Right")
    if left is None or right is None:
        return None
    return [left.thumb_tip, left.index_tip, right.index_tip, right.thumb_tip]


def build_mask(points: List[Tuple[int, int]], frame_shape: Tuple[int, int, int]) -> np.ndarray:
    """Gefüllte Maske des durch die 4 Punkte (in fester Reihenfolge) aufgespannten
    Vierecks, mit weicher Kante."""
    h, w = frame_shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)

    pts = np.array(points, dtype=np.int32)
    cv2.fillPoly(mask, [pts], 255)

    ksize = config.QUAD_MASK_FEATHER | 1
    mask = cv2.GaussianBlur(mask, (ksize, ksize), 0)
    return mask
