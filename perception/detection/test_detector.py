import cv2

from perception.detection.detector import VehicleDetector


IMAGE_PATH = "data/videos/test1.jpg"


def main():

    image = cv2.imread(IMAGE_PATH)

    if image is None:
        print(f"Could not open image: {IMAGE_PATH}")
        return

    detector = VehicleDetector()

    detections = detector.detect(image)

    print("=" * 40)
    print("FLOWMIND DETECTION TEST")
    print("=" * 40)

    print(f"Vehicles detected: {len(detections)}")

    for index, vehicle in enumerate(
        detections,
        start=1
    ):

        print(
            f"{index}. "
            f"{vehicle['class_name']} | "
            f"confidence={vehicle['confidence']:.2f}"
        )


if __name__ == "__main__":
    main()