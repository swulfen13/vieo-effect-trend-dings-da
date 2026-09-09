import numpy as np


def apply(frame, mask, points, frame_index):
    """VHS-artiges Rauschen + gelegentliches Zeilenflackern innerhalb der Flächen-Maske."""
    h, w = frame.shape[:2]
    rng = np.random.default_rng(frame_index)

    noise = rng.integers(-45, 46, size=(h, w, 1)).astype(np.float32)
    noisy = frame.astype(np.float32) + noise

    if frame_index % 5 == 0:
        row = int(rng.integers(0, h))
        band_h = max(2, h // 90)
        noisy[row : row + band_h] = 255 - noisy[row : row + band_h]

    alpha = (mask.astype(np.float32) / 255.0)[..., None]
    out = noisy * alpha + frame.astype(np.float32) * (1 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)
