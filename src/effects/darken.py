import numpy as np

_DARKEN_FACTOR = 0.14


def apply(frame, mask, points, frame_index):
    """Abgedunkelter Bereich innerhalb der Flächen-Maske."""
    darkened = frame.astype(np.float32) * _DARKEN_FACTOR

    alpha = (mask.astype(np.float32) / 255.0)[..., None]
    out = darkened * alpha + frame.astype(np.float32) * (1 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)
