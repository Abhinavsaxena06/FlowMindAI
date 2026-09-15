import cv2
import time
import json

from backend.flowmind_engine import (
    FlowMindEngine
)


def main():

    engine = FlowMindEngine()

    source = (
        "data/videos/traffic.mp4"
    )

    capture = cv2.VideoCapture(
        source
    )

    if not capture.isOpened():

        raise RuntimeError(
            f"Could not open source: {source}"
        )

    print()
    print(
        "=========================================="
    )
    print(
        "      FLOWMIND LIVE PIPELINE"
    )
    print(
        "=========================================="
    )

    print(
        f"Source: {source}"
    )

    print(
        "Press Q to stop."
    )

    print(
        "=========================================="
    )

    processing_interval = (
        1.0 / 8.0
    )

    last_processed = 0.0

    while True:

        success, frame = (
            capture.read()
        )

        if not success:

            print(
                "[FlowMind] Video ended."
            )

            break

        current_time = time.time()

        if (
            current_time -
            last_processed
            <
            processing_interval
        ):

            continue

        last_processed = (
            current_time
        )

        (
            processed_frame,
            state,
            forecast,
            recommendation
        ) = engine.process_frame(

            frame,

            current_time
        )

        # ---------------------------------------------
        # Display recommendation
        # ---------------------------------------------

        if recommendation:

            strategy = (
                recommendation[
                    "recommended_strategy"
                ]
            )

            phase = strategy[
                "phase"
            ]

            action = strategy[
                "action"
            ]

            duration = strategy[
                "duration_seconds"
            ]

            text = (
                f"FLOWMIND: "
                f"{action} "
                f"{phase.upper()} "
                f"{duration}s"
            )

            cv2.putText(

                processed_frame,

                text,

                (
                    20,
                    processed_frame.shape[0]
                    - 30
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.7,

                (0, 255, 255),

                2
            )

        cv2.imshow(

            "FlowMind - Camera Intelligence",

            processed_frame
        )

        # ---------------------------------------------
        # Print AI result
        # ---------------------------------------------

        if recommendation:

            print()

            print(
                "FLOWMIND DECISION:"
            )

            print(
                json.dumps(
                    recommendation[
                        "recommended_strategy"
                    ],
                    indent=2
                )
            )

        key = cv2.waitKey(1)

        if key & 0xFF == ord("q"):

            break

    capture.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":

    main()