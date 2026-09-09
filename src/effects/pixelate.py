import cv2
import numpy as np

_BLOCK_SIZE = 32


def apply(frame, mask, points, frame_index):
    """Verpixelter Bereich innerhalb der Flächen-Maske."""
    h, w = frame.shape[:2]
    small_w = max(1, w // _BLOCK_SIZE)
    small_h = max(1, h // _BLOCK_SIZE)

    small = cv2.resize(frame, (small_w, small_h), interpolation=cv2.INTER_LINEAR)
    pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST).astype(np.float32)

    alpha = (mask.astype(np.float32) / 255.0)[..., None]
    out = pixelated * alpha + frame.astype(np.float32) * (1 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)
