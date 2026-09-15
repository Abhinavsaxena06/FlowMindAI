from backend.perception.live_traffic import (
    LiveTrafficEngine
)


def main():

    engine = LiveTrafficEngine()

    engine.run(
        show=True,
        save_output=True
    )


if __name__ == "__main__":
    main()