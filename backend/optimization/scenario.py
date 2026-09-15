from copy import deepcopy

from backend.digital_twin.simulator import (
    DigitalTwinSimulator
)


class ScenarioRunner:

    def __init__(
        self,
        traffic_state,
        forecast
    ):

        self.traffic_state = deepcopy(
            traffic_state
        )

        self.forecast = deepcopy(
            forecast
        )

    # =========================================================
    # CREATE FUTURE STATE
    # =========================================================

    def create_scenario_state(
        self
    ):

        state = deepcopy(
            self.traffic_state
        )

        forecast_approaches = (
            self.forecast.get(
                "approaches",
                {}
            )
        )

        for approach, data in (
            state.get(
                "approaches",
                {}
            ).items()
        ):

            prediction = (
                forecast_approaches.get(
                    approach,
                    {}
                )
            )

            if "predicted_vehicles" in prediction:

                data["predicted_vehicles"] = (
                    prediction[
                        "predicted_vehicles"
                    ]
                )

            if "predicted_queue" in prediction:

                data["predicted_queue"] = (
                    prediction[
                        "predicted_queue"
                    ]
                )

        return state

    # =========================================================
    # RUN ONE SCENARIO
    # =========================================================

    def run(
        self,
        strategy,
        duration_seconds=60
    ):

        state = (
            self.create_scenario_state()
        )

        simulator = (
            DigitalTwinSimulator(
                state,
                self.forecast
            )
        )

        simulator.junction.set_phase(
            strategy["phase"]
        )

        metrics = simulator.run(
            duration_seconds
        )

        return {

            "strategy":
                strategy,

            "metrics":
                metrics
        }

    # =========================================================
    # STRATEGIES
    # =========================================================

    def generate_strategies(self):

        strategies = []

        approaches = [
            "north",
            "east",
            "south",
            "west"
        ]

        for approach in approaches:

            strategies.append({

                "phase":
                    approach,

                "action":
                    "HOLD_GREEN",

                "duration_seconds":
                    10
            })

            strategies.append({

                "phase":
                    approach,

                "action":
                    "EXTEND_GREEN",

                "duration_seconds":
                    20
            })

            strategies.append({

                "phase":
                    approach,

                "action":
                    "EXTEND_GREEN",

                "duration_seconds":
                    30
            })

        return strategies

    # =========================================================
    # RUN ALL
    # =========================================================

    def run_all(
        self,
        duration_seconds=60
    ):

        strategies = (
            self.generate_strategies()
        )

        results = []

        for strategy in strategies:

            result = self.run(
                strategy,
                duration_seconds
            )

            results.append(
                result
            )

        return results