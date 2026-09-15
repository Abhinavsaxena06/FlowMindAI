from threading import Thread

from backend.app.core.state_manager import (
    traffic_state_manager
)

from traffic.video_processor import (
    TrafficVideoProcessor
)


processor_thread = None


def get_current_traffic():

    return traffic_state_manager.get_state()


def update_traffic_state(
    state
):

    traffic_state_manager.update(
        state
    )

    return state


def start_video_processing(
    video_path="data/videos/traffic.mp4",
    model_path="models/yolov8m.pt"
):

    global processor_thread

    if (
        processor_thread
        and
        processor_thread.is_alive()
    ):

        return {
            "status": "already_running"
        }

    def worker():

        processor = (
            TrafficVideoProcessor(
                video_path=video_path,
                model_path=model_path,
                output_path=(
                    "data/processed/"
                    "flowmind_live.mp4"
                )
            )
        )

        processor.run(
            save_video=True
        )

    processor_thread = Thread(
        target=worker,
        daemon=True
    )

    processor_thread.start()

    return {
        "status": "started"
    }


def pipeline_status():

    global processor_thread

    if (
        processor_thread
        and
        processor_thread.is_alive()
    ):

        return {
            "running": True
        }

    return {
        "running": False
    }