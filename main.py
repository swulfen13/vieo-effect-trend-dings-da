import platform
import random

import cv2
import numpy as np

from src import config, region, ui
from src.effects import RANDOMIZABLE_EFFECTS, apply_effect
from src.hand_tracker import HandTracker
from src.virtual_cam import VirtualCam

_ACTIVE_OUTLINE_COLOR = (255, 255, 255)
_FROZEN_OUTLINE_COLOR = (140, 140, 140)


def _draw_quad_outline(frame, points, color):
    """Nur für die lokale Vorschau: dünner Umriss einer Effekt-Fläche."""
    pts = np.array(points, dtype=np.int32)
    cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=1, lineType=cv2.LINE_AA)


def _camera_backend():
    system = platform.system()
    if system == "Windows":
        return cv2.CAP_DSHOW
    if system == "Linux":
        return cv2.CAP_V4L2
    return cv2.CAP_ANY


class _GestureTrigger:
    """Edge-Trigger mit Cooldown für eine Pinch-Geste (löst nur auf dem Übergang
    nicht-gedrückt -> gedrückt aus, danach kurze Sperrzeit)."""

    def __init__(self, cooldown_frames: int):
        self._cooldown_frames = cooldown_frames
        self._was_active = False
        self._cooldown = 0

    def poll(self, is_active: bool) -> bool:
        triggered = False
        if self._cooldown > 0:
            self._cooldown -= 1
        elif is_active and not self._was_active:
            triggered = True
            self._cooldown = self._cooldown_frames
        self._was_active = is_active
        return triggered


def main():
    cap = cv2.VideoCapture(config.CAMERA_INDEX, _camera_backend())
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, config.TARGET_FPS)

    if not cap.isOpened():
        raise RuntimeError(
            f"Konnte Kamera {config.CAMERA_INDEX} nicht öffnen. Anderes Programm nutzt sie evtl. gerade."
        )

    ok, first_frame = cap.read()
    if not ok:
        raise RuntimeError("Konnte kein Bild von der Kamera lesen.")
    height, width = first_frame.shape[:2]

    tracker = HandTracker()
    vcam = VirtualCam(width, height, config.TARGET_FPS)

    mouse_state = {"clicked_effect": None}

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and x >= width:
            clicked = ui.hit_test(x - width, y)
            if clicked is not None:
                mouse_state["clicked_effect"] = clicked

    cv2.namedWindow(config.WINDOW_NAME)
    cv2.setMouseCallback(config.WINDOW_NAME, on_mouse)

    current_effect = config.DEFAULT_EFFECT
    frame_index = 0
    frozen_zones = []  # [{"points": [(x,y)*4], "effect": name}]

    randomize_trigger = _GestureTrigger(config.GESTURE_COOLDOWN_FRAMES)
    freeze_trigger = _GestureTrigger(config.GESTURE_COOLDOWN_FRAMES)
    clear_trigger = _GestureTrigger(config.GESTURE_COOLDOWN_FRAMES)

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("[main] Kein Kamerabild mehr, beende.")
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            hands = tracker.process(rgb, width, height)
            quad_points = region.get_quad_points(hands)
            right_hand, left_hand = hands.get("Right"), hands.get("Left")

            if randomize_trigger.poll(any(h.index_pinching for h in hands.values())):
                current_effect = random.choice(RANDOMIZABLE_EFFECTS)

            if freeze_trigger.poll(right_hand is not None and right_hand.middle_pinching):
                if quad_points is not None:
                    frozen_zones.append({"points": list(quad_points), "effect": current_effect})
                    if len(frozen_zones) > config.MAX_FROZEN_ZONES:
                        frozen_zones.pop(0)

            if clear_trigger.poll(left_hand is not None and left_hand.middle_pinching):
                frozen_zones.clear()

            if mouse_state["clicked_effect"] is not None:
                current_effect = mouse_state["clicked_effect"]
                mouse_state["clicked_effect"] = None

            # Sauberer Effekt-Frame ohne jede Debug-Markierung -> geht 1:1 an die
            # virtuelle Kamera. Sieht normal aus, solange keine Flaeche aktiv/eingefroren ist.
            clean_frame = frame
            for zone in frozen_zones:
                mask = region.build_mask(zone["points"], frame.shape)
                clean_frame = apply_effect(zone["effect"], clean_frame, mask, zone["points"], frame_index)

            if quad_points is not None:
                mask = region.build_mask(quad_points, frame.shape)
                clean_frame = apply_effect(current_effect, clean_frame, mask, quad_points, frame_index)

            vcam.send(clean_frame)

            # Vorschau bekommt zusaetzlich Umrisse + Sidebar, nur lokal sichtbar.
            display_frame = clean_frame.copy()
            for zone in frozen_zones:
                _draw_quad_outline(display_frame, zone["points"], _FROZEN_OUTLINE_COLOR)
            if quad_points is not None:
                _draw_quad_outline(display_frame, quad_points, _ACTIVE_OUTLINE_COLOR)

            sidebar = ui.build_sidebar(height, current_effect, len(hands), vcam.available, len(frozen_zones))
            combined = np.hstack([display_frame, sidebar])
            cv2.imshow(config.WINDOW_NAME, combined)

            key = cv2.waitKey(1) & 0xFF
            if key in config.KEY_QUIT:
                break
            elif key == config.KEY_RANDOMIZE:
                current_effect = random.choice(RANDOMIZABLE_EFFECTS)
            elif key in config.KEY_EFFECT_MAP:
                current_effect = config.KEY_EFFECT_MAP[key]

            frame_index += 1
    finally:
        cap.release()
        tracker.close()
        vcam.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
