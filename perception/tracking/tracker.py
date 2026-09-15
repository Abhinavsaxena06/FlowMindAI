from ultralytics import YOLO


class VehicleTracker:

    VEHICLE_CLASSES = [
        1,
        2,
        3,
        5,
        7
    ]

    def __init__(
        self,
        model_path="models/yolov8m.pt",
        tracker_config="bytetrack.yaml",
        confidence=0.25
    ):

        self.model = YOLO(
            model_path
        )

        self.tracker_config = (
            tracker_config
        )

        self.confidence = confidence

    def track(
        self,
        frame
    ):

        results = self.model.track(

            source=frame,

            persist=True,

            tracker=self.tracker_config,

            conf=self.confidence,

            classes=self.VEHICLE_CLASSES,

            verbose=False
        )

        tracks = []

        if not results:
            return tracks

        result = results[0]

        if result.boxes is None:
            return tracks

        boxes = result.boxes

        if boxes.id is None:
            return tracks

        ids = (
            boxes.id
            .int()
            .cpu()
            .tolist()
        )

        coordinates = (
            boxes.xyxy
            .cpu()
            .numpy()
        )

        classes = (
            boxes.cls
            .int()
            .cpu()
            .tolist()
        )

        confidences = (
            boxes.conf
            .cpu()
            .numpy()
        )

        class_names = {
            1: "bicycle",
            2: "car",
            3: "motorcycle",
            5: "bus",
            7: "truck"
        }

        for i, track_id in enumerate(ids):

            x1, y1, x2, y2 = (
                coordinates[i]
            )

            class_id = classes[i]

            confidence = float(
                confidences[i]
            )

            tracks.append({

                "track_id":
                    int(track_id),

                "class_id":
                    int(class_id),

                "class_name":
                    class_names.get(
                        class_id,
                        "unknown"
                    ),

                "confidence":
                    round(
                        confidence,
                        4
                    ),

                "x1":
                    float(x1),

                "y1":
                    float(y1),

                "x2":
                    float(x2),

                "y2":
                    float(y2),

                "x1":
                    float(x1),

                "y1":
                    float(y1),

                "x2":
                    float(x2),

                "y2":
                    float(y2),

                "bbox": [
                    float(x1),
                    float(y1),
                    float(x2),
                    float(y2)
                ],

                "center_x":
                    float(
                        (x1 + x2) / 2
                    ),

                "center_y":
                    float(
                        (y1 + y2) / 2
                    )
            })

        return tracks