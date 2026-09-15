import json
import time

from backend.prediction.predictor import (
    TrafficPredictor
)

from backend.prediction.forecast import (
    TrafficForecast
)

from backend.optimization.scenario import (
    ScenarioRunner
)

from backend.optimization.strategy_selector import (
    StrategySelector
)


def create_state(
    north,
    east,
    south,
    west
):

    return {

        "junction":
            "JUNCTION-A",

        "approaches": {

            "north": {

                "vehicles":
                    north,

                "queue":
                    max(
                        0,
                        north - 7
                    ),

                "avg_speed_kmh":
                    15
            },

            "east": {

                "vehicles":
                    east,

                "queue":
                    max(
                        0,
                        east - 4
                    ),

                "avg_speed_kmh":
                    23
            },

            "south": {

                "vehicles":
                    south,

                "queue":
                    max(
                        0,
                        south - 5
                    ),

                "avg_speed_kmh":
                    18
            },

            "west": {

                "vehicles":
                    west,

                "queue":
                    max(
                        0,
                        west - 3
                    ),

                "avg_speed_kmh":
                    26
            }
        }
    }


def main():

    predictor = (
        TrafficPredictor()
    )

    print()
    print(
        "=========================================="
    )
    print(
        "       FLOWMIND PREDICTION ENGINE"
    )
    print(
        "=========================================="
    )
    print()

    # Simulate traffic arriving from camera
    traffic_states = [

        create_state(
            10,
            6,
            8,
            4
        ),

        create_state(
            13,
            6,
            9,
            4
        ),

        create_state(
            16,
            7,
            10,
            5
        ),

        create_state(
            19,
            7,
            11,
            5
        ),

        create_state(
            22,
            8,
            12,
            6
        )
    ]

    for state in traffic_states:

        predictor.add_state(
            state
        )

        time.sleep(
            0.1
        )

    forecast_engine = (
        TrafficForecast(
            predictor
        )
    )

    forecast = (
        forecast_engine.generate(
            horizon_seconds=60
        )
    )

    print(
        "60 SECOND FORECAST:"
    )

    print(
        json.dumps(
            forecast,
            indent=2
        )
    )

    # ---------------------------------------------------------
    # CURRENT STATE
    # ---------------------------------------------------------

    current_state = (
        traffic_states[-1]
    )

    # ---------------------------------------------------------
    # RUN SCENARIOS
    # ---------------------------------------------------------

    scenario_runner = (
        ScenarioRunner(

            current_state,

            forecast
        )
    )

    results = (
        scenario_runner.run_all(
            duration_seconds=60
        )
    )

    # ---------------------------------------------------------
    # SELECT
    # ---------------------------------------------------------

    selector = (
        StrategySelector()
    )

    recommendation = (
        selector.select(
            results
        )
    )

    print()
    print(
        "=========================================="
    )

    print(
        "FLOWMIND RECOMMENDATION"
    )

    print(
        "=========================================="
    )

    print(
        json.dumps(
            recommendation,
            indent=2
        )
    )


if __name__ == "__main__":
    main()