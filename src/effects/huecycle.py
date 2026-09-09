import cv2
import numpy as np

_SPEED = 4  # Grad Farbtondrehung pro Frame


def apply(frame, mask, points, frame_index):
    """Durchlaufender Regenbogen-Farbton (psychedelischer Effekt) innerhalb der Flächen-Maske."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.int32)
    hsv[..., 0] = (hsv[..., 0] + frame_index * _SPEED) % 180
    cycled = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)

    alpha = (mask.astype(np.float32) / 255.0)[..., None]
    out = cycled * alpha + frame.astype(np.float32) * (1 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)
