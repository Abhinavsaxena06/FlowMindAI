import json

from backend.digital_twin.simulator import (
    DigitalTwinSimulator
)


def create_test_state():

    return {

        "junction": "JUNCTION-A",

        "approaches": {

            "north": {
                "vehicles": 18,
                "queue": 11,
                "stopped": 8,
                "density": 0.72,
                "avg_speed_kmh": 14.2
            },

            "east": {
                "vehicles": 7,
                "queue": 3,
                "stopped": 2,
                "density": 0.31,
                "avg_speed_kmh": 25.8
            },

            "south": {
                "vehicles": 12,
                "queue": 7,
                "stopped": 5,
                "density": 0.52,
                "avg_speed_kmh": 18.4
            },

            "west": {
                "vehicles": 5,
                "queue": 2,
                "stopped": 1,
                "density": 0.24,
                "avg_speed_kmh": 27.1
            }
        }
    }


def main():

    state = create_test_state()

    print()
    print(
        "=========================================="
    )
    print(
        "       FLOWMIND DIGITAL TWIN"
    )
    print(
        "=========================================="
    )

    print()

    print(
        "LIVE TRAFFIC STATE:"
    )

    print(
        json.dumps(
            state,
            indent=2
        )
    )

    print()

    simulator = (
        DigitalTwinSimulator(
            state
        )
    )

    # Start with North green.
    simulator.junction.set_phase(
        "north"
    )

    print(
        "Current signal phase: NORTH GREEN"
    )

    print()

    metrics = simulator.run(
        duration_seconds=60
    )

    print(
        "SIMULATION RESULTS:"
    )

    print(
        json.dumps(
            metrics,
            indent=2
        )
    )

    print()
    print(
        "=========================================="
    )


if __name__ == "__main__":
    main()