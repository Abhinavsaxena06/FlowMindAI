import cv2
import threading
import time
from typing import Optional

from backend.flowmind_engine import FlowMindEngine


class TrafficRuntime:

    """
    Persistent background runtime for FlowMind.

    It continuously reads:

        video file
        webcam
        RTSP camera

    and feeds frames into FlowMindEngine.
    """

    def __init__(self):

        self.engine = FlowMindEngine(
            state_interval_seconds=1.0,
            prediction_horizon_seconds=60,
        )

        self.capture = None

        self.thread = None

        self.stop_event = threading.Event()

        self.lock = threading.Lock()

        # ---------------------------------------------------------
        # Runtime state
        # ---------------------------------------------------------

        self.running = False

        self.source = None

        self.started_at = None

        self.last_frame_time = None

        self.last_error = None

        self.frames_processed = 0

        self.latest_frame = None

    # =============================================================
    # SOURCE PARSER
    # =============================================================

    def _parse_source(self, source):

        if source is None:
            source = "data/videos/traffic.mp4"

        # Webcam:
        #
        # "0"
        # "1"
        # etc.

        if isinstance(source, str):

            if source.isdigit():
                return int(source)

        return source

    # =============================================================
    # START
    # =============================================================

    def start(
        self,
        source: Optional[str] = None,
    ):

        with self.lock:

            if self.running:

                return {
                    "status": "already_running",
                    "source": self.source,
                }

            self.source = (
                source
                or "data/videos/traffic.mp4"
            )

            parsed_source = self._parse_source(
                self.source
            )

            self.capture = cv2.VideoCapture(
                parsed_source
            )

            if not self.capture.isOpened():

                self.capture = None

                self.last_error = (
                    f"Could not open source: "
                    f"{self.source}"
                )

                return {
                    "status": "error",
                    "message": self.last_error,
                }

            # Reset FlowMind when a new source starts.
            self.engine.reset()

            self.stop_event.clear()

            self.running = True

            self.started_at = time.time()

            self.frames_processed = 0

            self.last_error = None

            self.thread = threading.Thread(
                target=self._worker,
                daemon=True,
            )

            self.thread.start()

            return {
                "status": "started",
                "source": self.source,
            }

    # =============================================================
    # STOP
    # =============================================================

    def stop(self):

        with self.lock:

            if not self.running:

                return {
                    "status": "not_running"
                }

            self.stop_event.set()

            self.running = False

        if self.thread:

            self.thread.join(
                timeout=3
            )

        with self.lock:

            if self.capture:

                self.capture.release()

                self.capture = None

            self.thread = None

        return {
            "status": "stopped"
        }

    # =============================================================
    # WORKER
    # =============================================================

    def _worker(self):

        try:

            while not self.stop_event.is_set():

                if self.capture is None:
                    break

                success, frame = (
                    self.capture.read()
                )

                # -------------------------------------------------
                # End of video
                # -------------------------------------------------

                if not success:

                    # For a video file, restart automatically.
                    #
                    # This makes the demo continuously run.

                    if isinstance(
                        self.source,
                        str
                    ) and not self.source.isdigit():

                        self.capture.set(
                            cv2.CAP_PROP_POS_FRAMES,
                            0
                        )

                        continue

                    break

                # -------------------------------------------------
                # FlowMind
                # -------------------------------------------------

                result = self.engine.process_frame(
                    frame,
                    timestamp=time.time()
                )

                annotated_frame = result.get(
                    "frame"
                )

                if annotated_frame is not None:

                    with self.lock:

                        self.latest_frame = (
                            annotated_frame.copy()
                        )

                self.frames_processed += 1

                self.last_frame_time = (
                    time.time()
                )

                # -------------------------------------------------
                # Respect video FPS
                # -------------------------------------------------

                fps = self.capture.get(
                    cv2.CAP_PROP_FPS
                )

                if fps is None or fps <= 0:

                    fps = 8.0

                delay = (
                    1.0 / fps
                )

                time.sleep(
                    min(delay, 0.20)
                )

        except Exception as error:

            with self.lock:

                self.last_error = str(
                    error
                )

        finally:

            with self.lock:

                self.running = False

    # =============================================================
    # STATUS
    # =============================================================

    def get_status(self):

        with self.lock:

            return {

                "running":
                    self.running,

                "source":
                    self.source,

                "started_at":
                    self.started_at,

                "last_frame_time":
                    self.last_frame_time,

                "frames_processed":
                    self.frames_processed,

                "last_error":
                    self.last_error,

                "engine":
                    self.engine.get_status(),
            }

    # =============================================================
    # LATEST RESULT
    # =============================================================

    def get_latest_result(self):

        with self.lock:

            return (
                self.engine
                .get_latest_result()
            )

    # =============================================================
    # STATE
    # =============================================================

    def get_state(self):

        with self.lock:

            return (
                self.engine
                .get_latest_state()
            )

    # =============================================================
    # FORECAST
    # =============================================================

    def get_forecast(self):

        with self.lock:

            return (
                self.engine
                .get_latest_forecast()
            )

    # =============================================================
    # RECOMMENDATION
    # =============================================================

    def get_recommendation(self):

        with self.lock:

            return (
                self.engine
                .get_latest_recommendation()
            )

    # =============================================================
    # LATEST FRAME
    # =============================================================

    def get_latest_frame(self):

        with self.lock:

            if self.latest_frame is None:

                return None

            return self.latest_frame.copy()


# Singleton runtime.
#
# FastAPI and all endpoints use the same instance.

traffic_runtime = TrafficRuntime()