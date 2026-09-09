import numpy as np

_LEVELS = 4
_STEP = 256 // _LEVELS


def apply(frame, mask, points, frame_index):
    """Starke Farbreduktion (Comic-/Poster-Look) innerhalb der Flächen-Maske."""
    posterized = (frame.astype(np.int32) // _STEP * _STEP).astype(np.float32)

    alpha = (mask.astype(np.float32) / 255.0)[..., None]
    out = posterized * alpha + frame.astype(np.float32) * (1 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)
