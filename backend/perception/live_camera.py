import cv2
import time

from backend.perception.live_traffic_engine import LiveTrafficEngine


def main():
    print("Starting webcam...")
    print("Press Q to quit.")

    engine = LiveTrafficEngine()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("ERROR: Could not open webcam.")
        return

    while True:
        success, frame = camera.read()

        if not success:
            print("ERROR: Could not read frame from webcam.")
            break

        timestamp = time.time()

        processed_frame, tracked_vehicles = engine.process_frame(
            frame,
            timestamp
        )

        cv2.putText(
            processed_frame,
            f"Vehicles: {len(tracked_vehicles)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "FlowMind Live Webcam",
            processed_frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()