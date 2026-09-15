import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2

from perception.detection.detector import VehicleDetector
from traffic.traffic_engine import TrafficEngine


IMAGE_PATH = "data/videos/test1.jpg"


def main():

    image = cv2.imread(IMAGE_PATH)

    if image is None:

        print(
            f"Could not load image: {IMAGE_PATH}"
        )

        return

    height, width = image.shape[:2]

    detector = VehicleDetector(
        model_path="yolov8m.pt"
    )

    detections = detector.detect(
        image
    )

    engine = TrafficEngine(
        frame_width=width,
        frame_height=height
    )

    state = engine.process(
        detections
    )

    print("\n================================")
    print("       FLOWMIND TRAFFIC STATE")
    print("================================")

    print(
        f"\nTotal vehicles: "
        f"{state['total_vehicles']}"
    )

    print("\nVehicle types:")

    for vehicle_type, count in (
        state["vehicle_types"].items()
    ):

        print(
            f"  {vehicle_type}: {count}"
        )

    print("\nLane counts:")

    for lane, data in (
        state["lanes"].items()
    ):

        print(
            f"  {lane}: "
            f"{data['vehicle_count']}"
        )


if __name__ == "__main__":
    main()