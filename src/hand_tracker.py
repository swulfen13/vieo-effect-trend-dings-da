import math
import time
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions

from . import config

_THUMB_TIP, _INDEX_TIP, _MIDDLE_TIP = 4, 8, 12
_WRIST, _MIDDLE_MCP = 0, 9


@dataclass
class HandCorners:
    thumb_tip: Tuple[int, int]
    index_tip: Tuple[int, int]
    index_pinching: bool  # Daumen+Zeigefinger nah -> zufaelliger Effektwechsel
    middle_pinching: bool  # Daumen+Mittelfinger nah -> Flaeche einfrieren/loeschen


class HandTracker:
    """Erkennt bis zu zwei Hände und liefert je Hand die geglättete Position von
    Daumen- und Zeigefingerspitze sowie zwei Pinch-Gesten (Daumen+Zeigefinger,
    Daumen+Mittelfinger). Die Glättung ist an das Handedness-Label (Left/Right)
    gebunden, damit sie beim Hände-Tauschen nicht springt."""

    def __init__(self, model_path: str = config.HAND_MODEL_PATH, num_hands: int = 2):
        options = vision.HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=num_hands,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self._landmarker = vision.HandLandmarker.create_from_options(options)
        self._start_time = time.monotonic()
        self._smoothed: Dict[str, Tuple[float, float]] = {}

    def close(self):
        self._landmarker.close()

    def _smooth(self, key: str, raw_point: Tuple[float, float]) -> Tuple[int, int]:
        if key not in self._smoothed:
            self._smoothed[key] = raw_point
        else:
            alpha = config.FINGERTIP_EMA_ALPHA
            prev_x, prev_y = self._smoothed[key]
            self._smoothed[key] = (
                prev_x + alpha * (raw_point[0] - prev_x),
                prev_y + alpha * (raw_point[1] - prev_y),
            )
        x, y = self._smoothed[key]
        return (int(x), int(y))

    @staticmethod
    def _hand_scale(landmarks) -> float:
        wrist, middle_mcp = landmarks[_WRIST], landmarks[_MIDDLE_MCP]
        return math.hypot(wrist.x - middle_mcp.x, wrist.y - middle_mcp.y) + 1e-6

    @classmethod
    def _is_pinching(cls, landmarks, tip_idx: int) -> bool:
        thumb, tip = landmarks[_THUMB_TIP], landmarks[tip_idx]
        pinch_dist = math.hypot(thumb.x - tip.x, thumb.y - tip.y)
        return (pinch_dist / cls._hand_scale(landmarks)) < config.PINCH_DISTANCE_RATIO

    def process(self, frame_rgb, frame_width: int, frame_height: int) -> Dict[str, HandCorners]:
        timestamp_ms = int((time.monotonic() - self._start_time) * 1000)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        result = self._landmarker.detect_for_video(mp_image, timestamp_ms)

        hands: Dict[str, HandCorners] = {}
        seen_labels = set()

        for landmarks, handedness in zip(result.hand_landmarks, result.handedness):
            label = handedness[0].category_name  # "Left" oder "Right"
            seen_labels.add(label)

            thumb_raw = (landmarks[_THUMB_TIP].x * frame_width, landmarks[_THUMB_TIP].y * frame_height)
            index_raw = (landmarks[_INDEX_TIP].x * frame_width, landmarks[_INDEX_TIP].y * frame_height)

            hands[label] = HandCorners(
                thumb_tip=self._smooth(f"{label}_thumb", thumb_raw),
                index_tip=self._smooth(f"{label}_index", index_raw),
                index_pinching=self._is_pinching(landmarks, _INDEX_TIP),
                middle_pinching=self._is_pinching(landmarks, _MIDDLE_TIP),
            )

        # Glättungs-Zustand für nicht mehr sichtbare Hände verwerfen, damit ein
        # späteres Wiedererscheinen nicht von der alten Position aus einschwingt.
        for key in list(self._smoothed.keys()):
            if key.split("_")[0] not in seen_labels:
                del self._smoothed[key]

        return hands
