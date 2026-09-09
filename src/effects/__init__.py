from . import (
    darken,
    edge,
    glitch,
    grayscale,
    huecycle,
    invert,
    pixelate,
    posterize,
    staticnoise,
    thermal,
    warp,
)


def _apply_combo(frame, mask, points, frame_index):
    warped = warp.apply(frame, mask, points, frame_index)
    return glitch.apply(warped, mask, points, frame_index)


# Registry: Effekt-Name -> Funktion(frame, mask, points, frame_index) -> frame
# Neue Effekte lassen sich hier einfach ergänzen, ohne main.py anzufassen.
EFFECTS = {
    "off": None,
    "glitch": glitch.apply,
    "warp": warp.apply,
    "combo": _apply_combo,
    "grayscale": grayscale.apply,
    "invert": invert.apply,
    "darken": darken.apply,
    "pixelate": pixelate.apply,
    "edge": edge.apply,
    "thermal": thermal.apply,
    "posterize": posterize.apply,
    "huecycle": huecycle.apply,
    "staticnoise": staticnoise.apply,
}

# Effekte, aus denen die Zufalls-Geste auswählt (ohne "off")
RANDOMIZABLE_EFFECTS = [name for name in EFFECTS if name != "off"]


def apply_effect(name, frame, mask, points, frame_index):
    fn = EFFECTS.get(name)
    if fn is None:
        return frame
    return fn(frame, mask, points, frame_index)
