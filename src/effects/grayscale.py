import cv2
import numpy as np


def apply(frame, mask, points, frame_index):
    """Schwarz-Weiß innerhalb der Flächen-Maske."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR).astype(np.float32)

    alpha = (mask.astype(np.float32) / 255.0)[..., None]
    out = gray_bgr * alpha + frame.astype(np.float32) * (1 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)
