import cv2
import numpy as np


def apply(frame, mask, points, frame_index):
    """Thermalkamera-Falschfarben innerhalb der Flächen-Maske."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET).astype(np.float32)

    alpha = (mask.astype(np.float32) / 255.0)[..., None]
    out = thermal * alpha + frame.astype(np.float32) * (1 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)
