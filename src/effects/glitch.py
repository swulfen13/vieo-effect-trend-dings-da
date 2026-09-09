import cv2
import numpy as np


def apply(frame, mask, points, frame_index):
    """RGB-Split + zufällige horizontale Band-Verschiebungen, geblendet über die Flächen-Maske."""
    h, w = frame.shape[:2]

    dx = int(8 + 16 * abs(np.sin(frame_index * 0.25)))
    b, g, r = cv2.split(frame)
    r_shift = np.roll(r, dx, axis=1)
    b_shift = np.roll(b, -dx, axis=1)
    glitched = cv2.merge([b_shift, g, r_shift]).astype(np.float32)

    rng = np.random.default_rng(frame_index)
    band_h = max(4, h // 40)
    for _ in range(7):
        y0 = int(rng.integers(0, max(1, h - band_h)))
        band_dx = int(rng.integers(-40, 41))
        glitched[y0 : y0 + band_h] = np.roll(glitched[y0 : y0 + band_h], band_dx, axis=1)

    alpha = (mask.astype(np.float32) / 255.0)[..., None]
    out = glitched * alpha + frame.astype(np.float32) * (1 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)
