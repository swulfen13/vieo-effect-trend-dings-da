import numpy as np


def apply(frame, mask, points, frame_index):
    """Invertierte Farben (Negativ) innerhalb der Flächen-Maske."""
    inverted = (255 - frame).astype(np.float32)

    alpha = (mask.astype(np.float32) / 255.0)[..., None]
    out = inverted * alpha + frame.astype(np.float32) * (1 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)
