import time
import cv2
from pathlib import Path

from perception.detection.detector import VehicleDetector


IMAGE_PATH = "data/videos/test1.jpg"

MODELS = [
    "yolov8n.pt",
    "yolov8s.pt",
    "yolov8m.pt",
]

OUTPUT_DIR = Path("data/videos/model_results")


def draw_detections(image, detections):

    result = image.copy()

    for detection in detections:

        x1, y1, x2, y2 = detection["bbox"]

        class_name = detection["class_name"]
        confidence = detection["confidence"]

        cv2.rectangle(
            result,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        label = f"{class_name} {confidence:.2f}"

        cv2.putText(
            result,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    return result


def main():

    image = cv2.imread(IMAGE_PATH)

    if image is None:
        print(f"Could not load image: {IMAGE_PATH}")
        return

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print()
    print("======================================")
    print("       FLOWMIND YOLO BENCHMARK")
    print("======================================")

    for model_name in MODELS:

        print()
        print(f"Testing {model_name}...")

        detector = VehicleDetector(
            model_path=model_name
        )

        start = time.perf_counter()

        detections = detector.detect(image)

        elapsed = time.perf_counter() - start

        fps = 1 / elapsed if elapsed > 0 else 0

        output_image = draw_detections(
            image,
            detections
        )

        output_path = (
            OUTPUT_DIR /
            f"{Path(model_name).stem}_result.jpg"
        )

        cv2.imwrite(
            str(output_path),
            output_image
        )

        print(f"Detections : {len(detections)}")
        print(f"Time       : {elapsed:.3f} seconds")
        print(f"Approx FPS : {fps:.2f}")
        print(f"Result     : {output_path}")

        print("Objects:")

        for detection in detections:

            print(
                f"  {detection['class_name']:<12} "
                f"{detection['confidence']:.2f}"
            )


if __name__ == "__main__":
    main()