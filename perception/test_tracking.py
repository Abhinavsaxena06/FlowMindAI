import cv2
from pathlib import Path

from ultralytics import YOLO


VIDEO_PATH = "data/videos/traffic.mp4"
OUTPUT_PATH = "data/videos/tracking_result.mp4"

MODEL_PATH = "yolov8m.pt"


VEHICLE_CLASSES = {
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}


def main():

    print()
    print("======================================")
    print("       FLOWMIND BYTE TRACK TEST")
    print("======================================")

    video = cv2.VideoCapture(VIDEO_PATH)

    if not video.isOpened():

        print(
            f"Could not open video: {VIDEO_PATH}"
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

    total_frames = int(
        video.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    print(f"Resolution : {width}x{height}")
    print(f"FPS        : {fps:.2f}")
    print(f"Frames     : {total_frames}")
    print(f"Model      : {MODEL_PATH}")

    Path(
        OUTPUT_PATH
    ).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )

    writer = cv2.VideoWriter(
        OUTPUT_PATH,
        fourcc,
        fps,
        (width, height)
    )

    if not writer.isOpened():

        print(
            "Could not create output video."
        )

        video.release()

        return

    model = YOLO(MODEL_PATH)

    processed_frames = 0

    # ----------------------------------------
    # Tracking statistics
    # ----------------------------------------

    unique_ids = set()

    track_frame_counts = {}

    class_counts = {}

    # ----------------------------------------
    # Process video
    # ----------------------------------------

    while True:

        success, frame = video.read()

        if not success:
            break

        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=0.25,
            verbose=False
        )

        for result in results:

            if result.boxes is None:
                continue

            boxes = result.boxes

            for i in range(len(boxes)):

                class_id = int(
                    boxes.cls[i]
                )

                # Ignore non-vehicle classes

                if class_id not in VEHICLE_CLASSES:
                    continue

                confidence = float(
                    boxes.conf[i]
                )

                x1, y1, x2, y2 = map(
                    int,
                    boxes.xyxy[i].tolist()
                )

                class_name = VEHICLE_CLASSES[
                    class_id
                ]

                # --------------------------------
                # Track ID
                # --------------------------------

                track_id = None

                if boxes.id is not None:

                    track_id = int(
                        boxes.id[i]
                    )

                    unique_ids.add(
                        track_id
                    )

                    # Count how many frames
                    # this ID has been visible

                    track_frame_counts[
                        track_id
                    ] = (
                        track_frame_counts.get(
                            track_id,
                            0
                        ) + 1
                    )

                # --------------------------------
                # Class statistics
                # --------------------------------

                class_counts[
                    class_name
                ] = (
                    class_counts.get(
                        class_name,
                        0
                    ) + 1
                )

                # --------------------------------
                # Draw bounding box
                # --------------------------------

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # --------------------------------
                # Draw label
                # --------------------------------

                if track_id is not None:

                    label = (
                        f"ID {track_id} "
                        f"{class_name} "
                        f"{confidence:.2f}"
                    )

                else:

                    label = (
                        f"{class_name} "
                        f"{confidence:.2f}"
                    )

                cv2.putText(
                    frame,
                    label,
                    (
                        x1,
                        max(y1 - 10, 20)
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 255, 0),
                    2
                )

        # ----------------------------------------
        # Progress
        # ----------------------------------------

        processed_frames += 1

        if processed_frames % 50 == 0:

            percentage = (
                processed_frames /
                total_frames *
                100
                if total_frames > 0
                else 0
            )

            print(
                f"Processed: "
                f"{processed_frames}/"
                f"{total_frames} "
                f"({percentage:.1f}%)"
            )

        writer.write(frame)

    # ----------------------------------------
    # Cleanup
    # ----------------------------------------

    video.release()
    writer.release()

    # ----------------------------------------
    # Final statistics
    # ----------------------------------------

    print()
    print("======================================")
    print("          TRACKING COMPLETED")
    print("======================================")

    print(
        f"Processed frames : "
        f"{processed_frames}"
    )

    print(
        f"Unique vehicle IDs: "
        f"{len(unique_ids)}"
    )

    print()
    print("Detection observations:")

    for class_name, count in sorted(
        class_counts.items()
    ):

        print(
            f"  {class_name:<12}: "
            f"{count}"
        )

    print()
    print("Longest tracked vehicles:")

    longest_tracks = sorted(
        track_frame_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )[:10]

    if longest_tracks:

        for track_id, frame_count in (
            longest_tracks
        ):

            duration = (
                frame_count / fps
            )

            print(
                f"  ID {track_id:<4} "
                f"{frame_count:>5} frames "
                f"({duration:.1f} sec)"
            )

    else:

        print(
            "  No tracking IDs were produced."
        )

    print()
    print(
        f"Result saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()