import cv2

from perception.tracking.tracker import VehicleTracker


VIDEO_PATH = "data/videos/traffic.mp4"


def main():

    video = cv2.VideoCapture(VIDEO_PATH)

    if not video.isOpened():
        print(f"Could not open video: {VIDEO_PATH}")
        return

    tracker = VehicleTracker()

    frame_number = 0

    while True:

        success, frame = video.read()

        if not success:
            break

        frame_number += 1

        vehicles = tracker.update(frame)

        print(
            f"Frame {frame_number}: "
            f"{len(vehicles)} vehicles"
        )

        if frame_number >= 30:
            break

    video.release()


if __name__ == "__main__":
    main()