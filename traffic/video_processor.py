import cv2
import json
import time
from pathlib import Path

from traffic.lane.lane_config import DEFAULT_LANES

from perception.tracking.tracker import (
    VehicleTracker
)

from traffic.tracking.trajectory import (
    TrajectoryTracker
)

from traffic.lane.zone_manager import (
    ZoneManager
)

from traffic.engine.traffic_engine import (
    TrafficEngine
)

from backend.app.core.state_manager import (
    traffic_state_manager
)


class TrafficVideoProcessor:

    def __init__(
        self,
        video_path,
        model_path="models/yolov8m.pt",
        output_path="data/processed/tracking_result.mp4",
        state_dir="data/traffic_states"
    ):

        self.video_path = video_path
        self.model_path = model_path
        self.output_path = output_path

        self.state_dir = Path(state_dir)

        self.state_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # --------------------------------------------------
        # TRACKER
        # --------------------------------------------------

        print("Loading vehicle tracking model...")

        self.tracker = VehicleTracker(
            model_path
        )

        print("Vehicle tracker loaded.")

        # --------------------------------------------------
        # TRAJECTORY
        # --------------------------------------------------

        self.trajectory = TrajectoryTracker()

        # --------------------------------------------------
        # ENGINE
        # --------------------------------------------------

        self.engine = None

        # --------------------------------------------------
        # ZONES
        # --------------------------------------------------

        self.zone_manager = None

        # --------------------------------------------------
        # VIDEO INFORMATION
        # --------------------------------------------------

        self.frame_number = 0
        self.fps = 30.0
        self.width = 0
        self.height = 0
        self.total_frames = 0

    # ======================================================
    # MAIN PIPELINE
    # ======================================================

    def run(
        self,
        save_video=True,
        max_frames=None
    ):

        print()
        print("Opening traffic video...")

        capture = cv2.VideoCapture(
            self.video_path
        )

        if not capture.isOpened():

            raise RuntimeError(
                f"Could not open video: "
                f"{self.video_path}"
            )

        # --------------------------------------------------
        # VIDEO PROPERTIES
        # --------------------------------------------------

        self.fps = capture.get(
            cv2.CAP_PROP_FPS
        )

        if self.fps <= 0:

            self.fps = 30.0

        self.width = int(
            capture.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        self.height = int(
            capture.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        self.total_frames = int(
            capture.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        duration = 0

        if self.fps > 0:

            duration = (
                self.total_frames
                / self.fps
            )

        print()
        print("VIDEO INFORMATION")
        print("-" * 60)
        print(
            f"Resolution : "
            f"{self.width} x {self.height}"
        )
        print(
            f"FPS        : "
            f"{self.fps:.2f}"
        )
        print(
            f"Frames     : "
            f"{self.total_frames}"
        )
        print(
            f"Duration   : "
            f"{duration:.2f} seconds"
        )
        print()

        # --------------------------------------------------
        # ZONE MANAGER
        # --------------------------------------------------

        self.zone_manager = ZoneManager(
            self.width,
            self.height
        )

        # --------------------------------------------------
        # TRAFFIC ENGINE
        # --------------------------------------------------

        self.engine = TrafficEngine(
            lanes=DEFAULT_LANES,
            fps=self.fps
        )

        # --------------------------------------------------
        # VIDEO WRITER
        # --------------------------------------------------

        writer = None

        if save_video:

            output = Path(
                self.output_path
            )

            output.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            fourcc = (
                cv2.VideoWriter_fourcc(
                    *"mp4v"
                )
            )

            writer = cv2.VideoWriter(
                str(output),
                fourcc,
                self.fps,
                (
                    self.width,
                    self.height
                )
            )

            if not writer.isOpened():

                capture.release()

                raise RuntimeError(
                    f"Could not create output video: "
                    f"{self.output_path}"
                )

        # --------------------------------------------------
        # STATE STORAGE
        # --------------------------------------------------

        states = []

        # --------------------------------------------------
        # PERFORMANCE
        # --------------------------------------------------

        start_time = time.time()

        last_progress_time = start_time

        # Print progress every N frames.
        progress_interval = max(
            1,
            int(self.fps * 2)
        )

        # --------------------------------------------------
        # PROCESS VIDEO
        # --------------------------------------------------

        print(
            "Starting FlowMind traffic analysis..."
        )

        print(
            "Progress will update every "
            "2 seconds."
        )

        print("-" * 60)

        try:

            while True:

                success, frame = (
                    capture.read()
                )

                if not success:

                    break

                self.frame_number += 1

                # --------------------------------------------------
                # MAX FRAME LIMIT
                # --------------------------------------------------

                if (
                    max_frames
                    and
                    self.frame_number
                    > max_frames
                ):

                    break

                # --------------------------------------------------
                # VEHICLE TRACKING
                # --------------------------------------------------

                tracks = self.tracker.track(
                    frame
                )

                # --------------------------------------------------
                # TIMESTAMP
                # --------------------------------------------------

                timestamp = (
                    self.frame_number
                    / self.fps
                )

                # --------------------------------------------------
                # TRAJECTORIES
                # --------------------------------------------------

                self.trajectory.update(
                    tracks
                )

                # --------------------------------------------------
                # LANE ASSIGNMENT
                # --------------------------------------------------

                lane_assignments = {}

                for track in tracks:

                    vehicle_id = track[
                        "track_id"
                    ]

                    lane = (
                        self.zone_manager.classify(
                            track["center_x"],
                            track["center_y"]
                        )
                    )

                    if lane == "INTERSECTION":

                        lane = (
                            self._infer_direction(
                                track
                            )
                        )

                    lane_assignments[
                        vehicle_id
                    ] = lane

                # --------------------------------------------------
                # TRAFFIC ENGINE
                # --------------------------------------------------

                traffic_state = (
                    self.engine.process(
                        tracks
                    )
                )

                # --------------------------------------------------
                # ADD PIPELINE METADATA
                # --------------------------------------------------

                traffic_state[
                    "frame_number"
                ] = self.frame_number

                traffic_state[
                    "video_time_seconds"
                ] = round(
                    timestamp,
                    2
                )

                traffic_state[
                    "vehicle_tracks"
                ] = self._serialize_tracks(
                    tracks,
                    lane_assignments
                )

                # --------------------------------------------------
                # UPDATE LIVE STATE
                # --------------------------------------------------

                traffic_state_manager.update(
                    traffic_state
                )

                # --------------------------------------------------
                # STORE STATE
                # --------------------------------------------------

                states.append(
                    traffic_state
                )

                # --------------------------------------------------
                # DRAW OUTPUT
                # --------------------------------------------------

                annotated = self.annotate(
                    frame,
                    tracks,
                    lane_assignments,
                    traffic_state
                )

                if writer:

                    writer.write(
                        annotated
                    )

                # --------------------------------------------------
                # PROGRESS
                # --------------------------------------------------

                current_time = time.time()

                if (
                    self.frame_number
                    % progress_interval
                    == 0
                ):

                    elapsed = (
                        current_time
                        - start_time
                    )

                    processing_fps = 0

                    if elapsed > 0:

                        processing_fps = (
                            self.frame_number
                            / elapsed
                        )

                    progress = 0

                    if self.total_frames > 0:

                        progress = (
                            self.frame_number
                            / self.total_frames
                        ) * 100

                    remaining_seconds = 0

                    if processing_fps > 0:

                        remaining_frames = max(
                            0,
                            self.total_frames
                            - self.frame_number
                        )

                        remaining_seconds = (
                            remaining_frames
                            / processing_fps
                        )

                    current_vehicles = (
                        traffic_state.get(
                            "total_vehicles",
                            len(tracks)
                        )
                    )

                    congestion = (
                        traffic_state.get(
                            "congestion_score",
                            0
                        )
                    )

                    status = (
                        traffic_state.get(
                            "traffic_status",
                            "UNKNOWN"
                        )
                    )

                    print(
                        f"\r"
                        f"Frame "
                        f"{self.frame_number}/"
                        f"{self.total_frames} "
                        f"| "
                        f"{progress:6.2f}% "
                        f"| "
                        f"FPS "
                        f"{processing_fps:5.2f} "
                        f"| "
                        f"Vehicles "
                        f"{current_vehicles:3d} "
                        f"| "
                        f"Congestion "
                        f"{congestion:5.1f} "
                        f"| "
                        f"{status:<12} "
                        f"| "
                        f"ETA "
                        f"{self._format_time(
                            remaining_seconds
                        )}",
                        end="",
                        flush=True
                    )

                    last_progress_time = (
                        current_time
                    )

            print()

        except KeyboardInterrupt:

            print()
            print(
                "Pipeline interrupted by user."
            )

        finally:

            capture.release()

            if writer:

                writer.release()

        # --------------------------------------------------
        # SAVE STATES
        # --------------------------------------------------

        self._save_summary(
            states
        )

        # --------------------------------------------------
        # FINAL STATISTICS
        # --------------------------------------------------

        elapsed = (
            time.time()
            - start_time
        )

        print()
        print("=" * 60)
        print("FLOWMIND PROCESSING COMPLETE")
        print("=" * 60)

        print(
            f"Frames processed : "
            f"{self.frame_number}"
        )

        print(
            f"States generated : "
            f"{len(states)}"
        )

        print(
            f"Processing time  : "
            f"{self._format_time(elapsed)}"
        )

        if elapsed > 0:

            print(
                f"Average FPS      : "
                f"{self.frame_number / elapsed:.2f}"
            )

        if save_video:

            print(
                f"Output video     : "
                f"{self.output_path}"
            )

        print(
            f"State file       : "
            f"{self.state_dir / 'latest_run.json'}"
        )

        print("=" * 60)

        return states

    # ======================================================
    # VIDEO ANNOTATION
    # ======================================================

    def annotate(
        self,
        frame,
        tracks,
        lane_assignments,
        state
    ):

        output = frame.copy()

        # --------------------------------------------------
        # VEHICLES
        # --------------------------------------------------

        for track in tracks:

            x1 = int(
                track["x1"]
            )

            y1 = int(
                track["y1"]
            )

            x2 = int(
                track["x2"]
            )

            y2 = int(
                track["y2"]
            )

            vehicle_id = track[
                "track_id"
            ]

            lane = lane_assignments.get(
                vehicle_id,
                "UNKNOWN"
            )

            class_name = track.get(
                "class_name",
                "vehicle"
            )

            confidence = track.get(
                "confidence",
                0
            )

            label = (
                f"{class_name} "
                f"ID:{vehicle_id} "
                f"{lane}"
            )

            # --------------------------------------------------
            # VEHICLE BOX
            # --------------------------------------------------

            cv2.rectangle(
                output,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # --------------------------------------------------
            # LABEL
            # --------------------------------------------------

            cv2.putText(
                output,
                label,
                (
                    x1,
                    max(
                        y1 - 8,
                        20
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (0, 255, 0),
                2
            )

            # --------------------------------------------------
            # CENTER POINT
            # --------------------------------------------------

            center_x = int(
                track.get(
                    "center_x",
                    (x1 + x2) / 2
                )
            )

            center_y = int(
                track.get(
                    "center_y",
                    (y1 + y2) / 2
                )
            )

            cv2.circle(
                output,
                (
                    center_x,
                    center_y
                ),
                4,
                (0, 255, 255),
                -1
            )

        # --------------------------------------------------
        # TRAFFIC INFORMATION
        # --------------------------------------------------

        score = state.get(
            "congestion_score",
            0
        )

        status = state.get(
            "traffic_status",
            "UNKNOWN"
        )

        vehicles = state.get(
            "total_vehicles",
            0
        )

        queue = state.get(
            "queue_count",
            0
        )

        speed = state.get(
            "average_speed",
            0
        )

        density = state.get(
            "density",
            0
        )

        # --------------------------------------------------
        # TOP DASHBOARD
        # --------------------------------------------------

        panel_height = 145

        cv2.rectangle(
            output,
            (10, 10),
            (430, panel_height),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            output,
            "FLOWMIND",
            (20, 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            2
        )

        cv2.putText(
            output,
            f"Vehicles: {vehicles}",
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        cv2.putText(
            output,
            f"Queue: {queue}",
            (150, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        cv2.putText(
            output,
            f"Speed: {speed:.1f} km/h",
            (270, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        cv2.putText(
            output,
            f"Congestion: {score:.1f}",
            (20, 92),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        cv2.putText(
            output,
            f"Density: {density:.2f}",
            (200, 92),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        cv2.putText(
            output,
            f"Status: {status}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        # --------------------------------------------------
        # FRAME NUMBER
        # --------------------------------------------------

        cv2.putText(
            output,
            f"Frame: {self.frame_number}",
            (
                max(
                    self.width - 180,
                    10
                ),
                30
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        return output

    # ======================================================
    # DIRECTION INFERENCE
    # ======================================================

    def _infer_direction(
        self,
        track
    ):

        x = track[
            "center_x"
        ]

        y = track[
            "center_y"
        ]

        center_x = (
            self.zone_manager.width
            / 2
        )

        center_y = (
            self.zone_manager.height
            / 2
        )

        # Determine direction based on
        # which side of the intersection
        # the vehicle is closest to.

        distance_top = y

        distance_bottom = (
            self.zone_manager.height
            - y
        )

        distance_left = x

        distance_right = (
            self.zone_manager.width
            - x
        )

        distances = {
            "NORTH": distance_top,
            "SOUTH": distance_bottom,
            "WEST": distance_left,
            "EAST": distance_right
        }

        return min(
            distances,
            key=distances.get
        )

    # ======================================================
    # SERIALIZE TRACKS
    # ======================================================

    def _serialize_tracks(
        self,
        tracks,
        lane_assignments
    ):

        result = []

        for track in tracks:

            item = track.copy()

            item["lane"] = (
                lane_assignments.get(
                    track["track_id"],
                    "UNKNOWN"
                )
            )

            result.append(
                item
            )

        return result

    # ======================================================
    # SAVE TRAFFIC HISTORY
    # ======================================================

    def _save_summary(
        self,
        states
    ):

        if not states:

            print(
                "WARNING: No traffic states "
                "were generated."
            )

            return

        summary_path = (
            self.state_dir
            / "latest_run.json"
        )

        # --------------------------------------------------
        # Create a lightweight state history.
        #
        # Vehicle-level tracks are removed from the
        # historical dataset because they make the file
        # unnecessarily large.
        # --------------------------------------------------

        history = []

        for state in states:

            clean_state = state.copy()

            clean_state.pop(
                "vehicle_tracks",
                None
            )

            clean_state.pop(
                "vehicles",
                None
            )

            history.append(
                clean_state
            )

        with open(
            summary_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                history,
                file,
                indent=2
            )

        print()
        print(
            f"Traffic history saved: "
            f"{summary_path}"
        )

    # ======================================================
    # TIME FORMATTER
    # ======================================================

    @staticmethod
    def _format_time(
        seconds
    ):

        seconds = max(
            0,
            int(seconds)
        )

        minutes = (
            seconds // 60
        )

        seconds = (
            seconds % 60
        )

        return (
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )