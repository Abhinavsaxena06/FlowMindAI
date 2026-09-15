from ultralytics import YOLO


class VehicleDetector:

    VEHICLE_CLASSES = {
        1: "bicycle",
        2: "car",
        3: "motorcycle",
        5: "bus",
        7: "truck"
    }

    def __init__(
        self,
        model_path="models/yolov8m.pt",
        confidence=0.25
    ):

        self.model_path = model_path
        self.confidence = confidence

        self.model = YOLO(
            model_path
        )

    def detect(
        self,
        frame
    ):

        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            verbose=False
        )

        detections = []

        if not results:
            return detections

        result = results[0]

        if result.boxes is None:
            return detections

        for box in result.boxes:

            class_id = int(
                box.cls[0].item()
            )

            confidence = float(
                box.conf[0].item()
            )

            if class_id not in self.VEHICLE_CLASSES:
                continue

            x1, y1, x2, y2 = (
                box.xyxy[0]
                .cpu()
                .numpy()
                .tolist()
            )

            detections.append({

                "class_id": class_id,

                "class_name":
                    self.VEHICLE_CLASSES[
                        class_id
                    ],

                "confidence":
                    round(
                        confidence,
                        4
                    ),

                "x1": float(x1),
                "y1": float(y1),
                "x2": float(x2),
                "y2": float(y2),
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
                    ),

                "width":
                    float(
                        x2 - x1
                    ),

                "height":
                    float(
                        y2 - y1
                    )
            })

        return detections