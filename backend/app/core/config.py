from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings:
    APP_NAME: str = os.getenv(
        "APP_NAME",
        "FlowMind"
    )

    VERSION: str = os.getenv(
        "VERSION",
        "1.0.0"
    )

    DEBUG: bool = os.getenv(
        "DEBUG",
        "true"
    ).lower() == "true"

    HOST: str = os.getenv(
        "HOST",
        "127.0.0.1"
    )

    PORT: int = int(
        os.getenv(
            "PORT",
            "8000"
        )
    )

    MODEL_PATH: str = os.getenv(
        "MODEL_PATH",
        "models/yolov8m.pt"
    )

    VIDEO_PATH: str = os.getenv(
        "VIDEO_PATH",
        "data/videos/traffic.mp4"
    )

    STATE_DIR: Path = PROJECT_ROOT / "data" / "traffic_states"

    PROCESSED_DIR: Path = PROJECT_ROOT / "data" / "processed"

    FRONTEND_URL: str = os.getenv(
        "FRONTEND_URL",
        "http://localhost:5173"
    )


settings = Settings()

settings.STATE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

settings.PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)