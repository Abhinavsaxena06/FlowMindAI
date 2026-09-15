import os
import time

from traffic.video_processor import TrafficVideoProcessor


VIDEO_PATH = "data/videos/traffic.mp4"
MODEL_PATH = "models/yolov8m.pt"
OUTPUT_PATH = "data/processed/flowmind_tracking.mp4"
STATE_DIR = "data/traffic_states"


def main():

    print()
    print("=" * 60)
    print("FLOWMIND TRAFFIC INTELLIGENCE PIPELINE")
    print("=" * 60)

    print(f"Video : {VIDEO_PATH}")
    print(f"Model : {MODEL_PATH}")
    print(f"Output: {OUTPUT_PATH}")
    print()

    # --------------------------------------------------
    # FILE CHECKS
    # --------------------------------------------------

    if not os.path.exists(VIDEO_PATH):

        print(
            f"ERROR: Video not found:\n"
            f"{VIDEO_PATH}"
        )

        return

    if not os.path.exists(MODEL_PATH):

        print(
            f"ERROR: Model not found:\n"
            f"{MODEL_PATH}"
        )

        return

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    os.makedirs(
        STATE_DIR,
        exist_ok=True
    )

    # --------------------------------------------------
    # INITIALIZE PROCESSOR
    # --------------------------------------------------

    print("Initializing FlowMind processor...")
    print()

    start_time = time.time()

    processor = TrafficVideoProcessor(
        video_path=VIDEO_PATH,
        model_path=MODEL_PATH,
        output_path=OUTPUT_PATH,
        state_dir=STATE_DIR
    )

    print()
    print("Processor initialized.")
    print()
    print("Starting traffic analysis...")
    print("-" * 60)

    # --------------------------------------------------
    # RUN PIPELINE
    # --------------------------------------------------

    states = processor.run(
        save_video=True
    )

    elapsed = (
        time.time()
        - start_time
    )

    # --------------------------------------------------
    # FINAL OUTPUT
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("FLOWMIND PIPELINE FINISHED")
    print("=" * 60)

    print(
        f"States generated : "
        f"{len(states)}"
    )

    print(
        f"Total runtime    : "
        f"{elapsed:.2f} seconds"
    )

    print(
        f"Output video     : "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Traffic history  : "
        f"{STATE_DIR}/latest_run.json"
    )

    # --------------------------------------------------
    # FILE VERIFICATION
    # --------------------------------------------------

    if os.path.exists(
        OUTPUT_PATH
    ):

        size_mb = (
            os.path.getsize(
                OUTPUT_PATH
            )
            /
            (1024 * 1024)
        )

        print(
            f"Output size      : "
            f"{size_mb:.2f} MB"
        )

    else:

        print(
            "WARNING: Output video "
            "was not created."
        )

    state_path = os.path.join(
        STATE_DIR,
        "latest_run.json"
    )

    if os.path.exists(
        state_path
    ):

        size_kb = (
            os.path.getsize(
                state_path
            )
            /
            1024
        )

        print(
            f"State file size  : "
            f"{size_kb:.2f} KB"
        )

    else:

        print(
            "WARNING: Traffic state "
            "file was not created."
        )

    print("=" * 60)


if __name__ == "__main__":
    main()