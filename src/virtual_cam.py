import pyvirtualcam


class VirtualCam:
    """Wrapper um pyvirtualcam mit Fallback, falls kein virtueller Kamera-Treiber
    (z.B. OBS Virtual Camera) installiert ist. In dem Fall läuft die App im
    reinen Preview-Modus weiter."""

    def __init__(self, width: int, height: int, fps: float):
        self._cam = None
        try:
            self._cam = pyvirtualcam.Camera(
                width=width, height=height, fps=fps, fmt=pyvirtualcam.PixelFormat.BGR
            )
            print(f"[virtual_cam] Aktiv: {self._cam.device}")
        except Exception as exc:
            print(
                "[virtual_cam] Kein virtueller Kamera-Treiber gefunden "
                f"({exc}). Läuft nur im Preview-Fenster. "
                "Für OBS/Zoom/Discord: OBS Studio installieren."
            )

    @property
    def available(self) -> bool:
        return self._cam is not None

    def send(self, frame_bgr) -> None:
        if self._cam is None:
            return
        self._cam.send(frame_bgr)
        self._cam.sleep_until_next_frame()

    def close(self) -> None:
        if self._cam is not None:
            self._cam.close()
