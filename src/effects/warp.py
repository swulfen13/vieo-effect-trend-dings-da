import cv2
import numpy as np

from .. import config

_RADIUS = config.WARP_RIPPLE_RADIUS


def apply(frame, mask, points, frame_index):
    """Ripple-Verzerrung ausgehend von den Eckpunkten, geblendet über die Flächen-Maske."""
    h, w = frame.shape[:2]
    map_x = np.tile(np.arange(w, dtype=np.float32), (h, 1))
    map_y = np.tile(np.arange(h, dtype=np.float32).reshape(-1, 1), (1, w))

    t = frame_index * 0.15
    for px, py in points:
        x0, x1 = max(0, px - _RADIUS), min(w, px + _RADIUS)
        y0, y1 = max(0, py - _RADIUS), min(h, py + _RADIUS)
        if x1 <= x0 or y1 <= y0:
            continue

        ys, xs = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        dxp = xs - px
        dyp = ys - py
        dist = np.sqrt(dxp**2 + dyp**2) + 1e-5
        falloff = np.clip(1 - dist / _RADIUS, 0, 1)
        wave = np.sin(dist * 0.25 - t * 4) * falloff * 28

        map_x[y0:y1, x0:x1] += (dxp / dist) * wave
        map_y[y0:y1, x0:x1] += (dyp / dist) * wave

    warped = cv2.remap(
        frame, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT
    )

    alpha = (mask.astype(np.float32) / 255.0)[..., None]
    out = warped.astype(np.float32) * alpha + frame.astype(np.float32) * (1 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)
