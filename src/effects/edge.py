import cv2
import numpy as np

_NEON_TINT_BGR = np.array([2.4, 1.7, 0.3], dtype=np.float32)  # cyan-grüner Neon-Ton
_BASE_DIM_FACTOR = 0.12


def apply(frame, mask, points, frame_index):
    """Dunkler Untergrund mit leuchtenden Kanten (Neon-Kontur) innerhalb der Flächen-Maske."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 150)
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR).astype(np.float32)
    neon = edges_bgr * _NEON_TINT_BGR

    base_dim = frame.astype(np.float32) * _BASE_DIM_FACTOR
    combined = np.clip(base_dim + neon, 0, 255)

    alpha = (mask.astype(np.float32) / 255.0)[..., None]
    out = combined * alpha + frame.astype(np.float32) * (1 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)
