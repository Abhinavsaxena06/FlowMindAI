import cv2

from perception.detection.detector import VehicleDetector


IMAGE_PATH = "data/videos/test1.jpg"
OUTPUT_PATH = "data/videos/detection_result.jpg"


def main():

    image = cv2.imread(IMAGE_PATH)

    if image is None:
        print(f"Could not load image: {IMAGE_PATH}")
        return

    detector = VehicleDetector()

    detections = detector.detect(image)

    print("\n==============================")
    print("FLOWMIND YOLO TEST")
    print("==============================")

    print(f"Vehicles detected: {len(detections)}")

    for i, detection in enumerate(detections, start=1):

        print(
            f"{i}. "
            f"{detection['class_name']} | "
            f"confidence={detection['confidence']:.2f}"
        )

        x1, y1, x2, y2 = detection["bbox"]

        # Draw bounding box
        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # Label
        label = (
            f"{detection['class_name']} "
            f"{detection['confidence']:.2f}"
        )

        cv2.putText(
            image,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    cv2.imwrite(
        OUTPUT_PATH,
        image
    )

    print("\nResult saved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()