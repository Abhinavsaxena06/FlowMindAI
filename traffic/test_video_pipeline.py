import cv2

from traffic.video_processor import (
    TrafficVideoProcessor
)
from traffic.tracking.trajectory import (
    TrajectoryTracker
)
from traffic.metrics.queue_detector import (
    QueueDetector
)


VIDEO_PATH = "data/videos/traffic.mp4"
OUTPUT_PATH = "data/videos/flowmind_tracking.mp4"

MODEL_PATH = "yolov8m.pt"


def main():

    print()
    print("======================================")
    print("       FLOWMIND VIDEO PIPELINE")
    print("======================================")

    video = cv2.VideoCapture(
        VIDEO_PATH
    )

    if not video.isOpened():

        print(
            f"Could not open: {VIDEO_PATH}"
        )

        return

    width = int(
        video.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    height = int(
        video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    fps = video.get(
        cv2.CAP_PROP_FPS
    )

    if fps <= 0:
        fps = 30

    processor = TrafficVideoProcessor(
        model_path=MODEL_PATH
    )

    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )
    trajectory_tracker = TrajectoryTracker(
    max_history=30
)
    queue_detector = QueueDetector(
    fps=fps,
    stationary_threshold=8.0,
    min_stationary_frames=15
)

    writer = cv2.VideoWriter(
        OUTPUT_PATH,
        fourcc,
        fps,
        (width, height)
    )

    frame_number = 0

    unique_ids = set()

    while True:

        success, frame = video.read()

        if not success:
            break

        tracked_vehicles = (
            processor.process_frame(
                frame
            )
        )
        trajectory_tracker.update(
        tracked_vehicles
        )
        queue_candidates = (
            queue_detector.update(
                tracked_vehicles,
                trajectory_tracker
            )
        )

        queue_counts = (
            queue_detector.count_by_lane(
                queue_candidates
            )
        )

        for vehicle in tracked_vehicles:

            track_id = vehicle["track_id"]

            if track_id is not None:

                unique_ids.add(
                    track_id
                )

        output = (
            processor.draw_tracks(
                frame,
                tracked_vehicles
            )
        )
        for vehicle in tracked_vehicles:

            track_id = vehicle["track_id"]

            if track_id is None:
                continue

            trajectory = (
                trajectory_tracker.get_trajectory(
                    track_id
                )
            )

            for i in range(
                1,
                len(trajectory)
            ):

                previous = trajectory[i - 1]
                current = trajectory[i]

                cv2.line(
                    output,
                    (
                        int(previous[0]),
                        int(previous[1])
                    ),
                    (
                        int(current[0]),
                        int(current[1])
                    ),
                    (255, 0, 0),
                    2
                )

        writer.write(output)

        frame_number += 1

        if frame_number % 50 == 0:

            print(
                f"Processed frames: "
                f"{frame_number}"
            )

    video.release()
    writer.release()

    print()
    print("======================================")
    print("             COMPLETED")
    print("======================================")

    print(
        f"Frames processed : {frame_number}"
    )

    print(
        f"Unique vehicles  : {len(unique_ids)}"
    )

    print(
        f"Output           : {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()