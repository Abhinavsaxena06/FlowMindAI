import cv2
import json
import time
import math
from pathlib import Path

from ultralytics import YOLO

from backend.perception.traffic_state import (
    TrafficStateEngine
)


class LiveTrafficEngine:

    def __init__(
        self,
        config_path="backend/perception/traffic_config.json"
    ):

        self.config_path = Path(
            config_path
        )

        with open(
            self.config_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.config = json.load(file)

        model_path = self.config[
            "model"
        ]["path"]

        confidence = self.config[
            "model"
        ]["confidence"]

        self.confidence = confidence

        print(
            f"[FlowMind] Loading model: {model_path}"
        )

        self.model = YOLO(
            model_path
        )

        print(
            "[FlowMind] YOLO model loaded."
        )

        speed_config = self.config[
            "speed"
        ]

        self.state_engine = (
            TrafficStateEngine(
                meters_per_pixel=
                speed_config[
                    "meters_per_pixel"
                ],

                queue_speed_kmh=
                self.config[
                    "queue"
                ]["queue_speed_kmh"]
            )
        )

        self.class_names = {
            int(class_id): name
            for class_id, name
            in self.config[
                "vehicle_classes"
            ].items()
        }

    # ---------------------------------------------------------
    # SOURCE
    # ---------------------------------------------------------

    def open_source(
        self,
        source
    ):

        print(
            f"[FlowMind] Opening source: {source}"
        )

        if isinstance(source, str):

            if source.isdigit():
                source = int(source)

        capture = cv2.VideoCapture(
            source
        )

        if not capture.isOpened():

            raise RuntimeError(
                f"Could not open camera/video: {source}"
            )

        return capture

    # ---------------------------------------------------------
    # NORMALIZED COORDINATES
    # ---------------------------------------------------------

    def normalize_point(
        self,
        x,
        y,
        width,
        height
    ):

        return (
            x / width,
            y / height
        )

    # ---------------------------------------------------------
    # POINT INSIDE POLYGON
    # ---------------------------------------------------------

    def point_inside_polygon(
        self,
        point,
        polygon
    ):

        x, y = point

        inside = False

        j = len(polygon) - 1

        for i in range(
            len(polygon)
        ):

            xi, yi = polygon[i]
            xj, yj = polygon[j]

            if (
                (yi > y)
                !=
                (yj > y)
            ):

                denominator = (
                    yj - yi
                )

                if denominator == 0:
                    denominator = 1e-9

                intersection_x = (
                    (xj - xi)
                    *
                    (y - yi)
                    /
                    denominator
                    +
                    xi
                )

                if x < intersection_x:

                    inside = not inside

            j = i

        return inside

    # ---------------------------------------------------------
    # FIND APPROACH
    # ---------------------------------------------------------

    def find_approach(
        self,
        normalized_x,
        normalized_y
    ):

        point = (
            normalized_x,
            normalized_y
        )

        for (
            approach,
            data
        ) in self.config[
            "approaches"
        ].items():

            polygon = data[
                "polygon"
            ]

            if self.point_inside_polygon(
                point,
                polygon
            ):

                return approach

        return None

    # ---------------------------------------------------------
    # STOP LINE
    # ---------------------------------------------------------

    def near_stop_line(
        self,
        approach,
        normalized_x,
        normalized_y
    ):

        if approach is None:
            return False

        stop_line = self.config[
            "approaches"
        ][approach][
            "stop_line"
        ]

        tolerance = 0.06

        if approach == "north":

            return (
                normalized_y
                >=
                stop_line - tolerance
            )

        if approach == "south":

            return (
                normalized_y
                <=
                stop_line + tolerance
            )

        if approach == "east":

            return (
                normalized_x
                <=
                stop_line + tolerance
            )

        if approach == "west":

            return (
                normalized_x
                >=
                stop_line - tolerance
            )

        return False

    # ---------------------------------------------------------
    # PROCESS FRAME
    # ---------------------------------------------------------

    def process_frame(
        self,
        frame,
        timestamp
    ):

        height, width = frame.shape[:2]

        results = self.model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=self.confidence,
            verbose=False
        )

        tracked_vehicles = []

        if not results:
            return frame, []

        result = results[0]

        boxes = result.boxes

        if boxes is None:
            return frame, []

        ids = None

        if boxes.id is not None:
            ids = boxes.id.cpu().tolist()

        classes = boxes.cls.cpu().tolist()
        confidences = boxes.conf.cpu().tolist()
        coordinates = boxes.xyxy.cpu().tolist()

        for index, box in enumerate(
            coordinates
        ):

            class_id = int(
                classes[index]
            )

            if class_id not in self.class_names:
                continue

            if ids is None:
                continue

            vehicle_id = int(
                ids[index]
            )

            confidence = float(
                confidences[index]
            )

            x1, y1, x2, y2 = box

            center_x = (
                x1 + x2
            ) / 2

            center_y = (
                y1 + y2
            ) / 2

            normalized_x, normalized_y = (
                self.normalize_point(
                    center_x,
                    center_y,
                    width,
                    height
                )
            )

            approach = (
                self.find_approach(
                    normalized_x,
                    normalized_y
                )
            )

            near_stop = (
                self.near_stop_line(
                    approach,
                    normalized_x,
                    normalized_y
                )
            )

            self.state_engine.update_vehicle(
                vehicle_id,
                center_x,
                center_y,
                timestamp
            )

            tracked_vehicles.append({

                "id": vehicle_id,

                "class": self.class_names[
                    class_id
                ],

                "class_id": class_id,

                "confidence": round(
                    confidence,
                    3
                ),

                "x": round(
                    center_x,
                    2
                ),

                "y": round(
                    center_y,
                    2
                ),

                "approach": approach,

                "near_stop_line":
                    near_stop
            })

            # Draw bounding box
            cv2.rectangle(
                frame,
                (
                    int(x1),
                    int(y1)
                ),
                (
                    int(x2),
                    int(y2)
                ),
                (0, 255, 0),
                2
            )

            label = (
                f"{self.class_names[class_id]}"
                f" ID:{vehicle_id}"
            )

            cv2.putText(
                frame,
                label,
                (
                    int(x1),
                    int(y1) - 8
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        return (
            frame,
            tracked_vehicles
        )

    # ---------------------------------------------------------
    # RUN
    # ---------------------------------------------------------

    def run(
        self,
        source=None,
        show=True,
        save_output=True
    ):

        if source is None:

            source = self.config[
                "camera"
            ]["source"]

        capture = self.open_source(
            source
        )

        fps = capture.get(
            cv2.CAP_PROP_FPS
        )

        if fps <= 0:
            fps = 25

        processing_fps = self.config[
            "camera"
        ].get(
            "processing_fps",
            8
        )

        frame_interval = (
            1.0 /
            processing_fps
        )

        output_path = (
            "data/videos/"
            "flowmind_live_result.mp4"
        )

        writer = None

        frame_width = int(
            capture.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        frame_height = int(
            capture.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        if save_output:

            fourcc = cv2.VideoWriter_fourcc(
                *"mp4v"
            )

            writer = cv2.VideoWriter(
                output_path,
                fourcc,
                processing_fps,
                (
                    frame_width,
                    frame_height
                )
            )

        print()
        print(
            "======================================"
        )
        print(
            "       FLOWMIND TRAFFIC ENGINE"
        )
        print(
            "======================================"
        )

        print(
            f"Source: {source}"
        )

        print(
            f"Processing FPS: {processing_fps}"
        )

        print(
            "Press Q to stop."
        )

        print(
            "======================================"
        )

        last_processed = 0

        latest_state = None

        while True:

            success, frame = (
                capture.read()
            )

            if not success:

                print(
                    "[FlowMind] Source ended."
                )

                break

            current_time = time.time()

            if (
                current_time -
                last_processed
                <
                frame_interval
            ):

                continue

            last_processed = (
                current_time
            )

            frame_timestamp = (
                current_time
            )

            processed_frame, vehicles = (
                self.process_frame(
                    frame,
                    frame_timestamp
                )
            )

            latest_state = (
                self.state_engine.build_state(
                    vehicles
                )
            )

            # Draw traffic-state information
            self.draw_state(
                processed_frame,
                latest_state
            )

            if writer is not None:

                writer.write(
                    processed_frame
                )

            if show:

                cv2.imshow(
                    "FlowMind - Live Traffic Intelligence",
                    processed_frame
                )

                key = cv2.waitKey(1)

                if key & 0xFF == ord("q"):
                    break

            print(
                json.dumps(
                    latest_state,
                    indent=2
                )
            )

        capture.release()

        if writer is not None:
            writer.release()

        cv2.destroyAllWindows()

        return latest_state

    # ---------------------------------------------------------
    # DRAW STATE
    # ---------------------------------------------------------

    def draw_state(
        self,
        frame,
        state
    ):

        y = 30

        cv2.putText(
            frame,
            "FLOWMIND LIVE TRAFFIC",
            (
                20,
                y
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        y += 35

        for (
            approach,
            data
        ) in state[
            "approaches"
        ].items():

            text = (
                f"{approach.upper()} | "
                f"Vehicles: {data['vehicles']} | "
                f"Queue: {data['queue']} | "
                f"Speed: {data['avg_speed_kmh']} km/h"
            )

            cv2.putText(
                frame,
                text,
                (
                    20,
                    y
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )

            y += 25


def main():

    engine = LiveTrafficEngine()

    engine.run(
        show=True,
        save_output=True
    )


if __name__ == "__main__":
    main()