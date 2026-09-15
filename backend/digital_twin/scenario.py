from copy import deepcopy

from .simulator import DigitalTwinSimulator


class ScenarioRunner:

    def __init__(
        self,
        traffic_state,
        forecast=None,
    ):

        self.traffic_state = deepcopy(
            traffic_state
        )

        self.forecast = deepcopy(
            forecast or {}
        )

    # =========================================================
    # CREATE SCENARIO STATE
    # =========================================================

    def create_scenario_state(self):

        scenario_state = deepcopy(
            self.traffic_state
        )

        forecast_approaches = (
            self.forecast.get(
                "approaches",
                {}
            )
        )

        for approach, data in (
            scenario_state
            .get(
                "approaches",
                {}
            )
            .items()
        ):

            forecast_data = (
                forecast_approaches.get(
                    approach,
                    {}
                )
            )

            data[
                "predicted_vehicles"
            ] = forecast_data.get(
                "predicted_vehicles",
                data.get(
                    "vehicles",
                    0
                )
            )

            data[
                "predicted_queue"
            ] = forecast_data.get(
                "predicted_queue",
                data.get(
                    "queue",
                    0
                )
            )

            data[
                "predicted_speed_kmh"
            ] = forecast_data.get(
                "predicted_speed_kmh",
                data.get(
                    "avg_speed_kmh",
                    0
                )
            )

        return scenario_state

    # =========================================================
    # RUN ONE SCENARIO
    # =========================================================

    def run(
        self,
        strategy,
        duration_seconds=60,
    ):

        scenario_state = (
            self.create_scenario_state()
        )

        simulator = (
            DigitalTwinSimulator(
                traffic_state=scenario_state,

                forecast=self.forecast,

                signal_plan=strategy,
            )
        )

        metrics = simulator.run(
            duration_seconds
        )

        return {
            "strategy": deepcopy(
                strategy
            ),

            "metrics": metrics,
        }

    # =========================================================
    # GENERATE STRATEGIES
    # =========================================================

    def generate_strategies(self):

        strategies = []

        approaches = [
            "north",
            "east",
            "south",
            "west",
        ]

        for approach in approaches:

            # Normal 10-second green.
            strategies.append({
                "phase": approach,

                "action": "HOLD_GREEN",

                "duration_seconds": 10,
            })

            # Extended 20-second green.
            strategies.append({
                "phase": approach,

                "action": "EXTEND_GREEN",

                "duration_seconds": 20,
            })

            # Extended 30-second green.
            strategies.append({
                "phase": approach,

                "action": "EXTEND_GREEN",

                "duration_seconds": 30,
            })

        return strategies

    # =========================================================
    # RUN ALL STRATEGIES
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
                strategy=strategy,

                duration_seconds=duration_seconds,
            )

            results.append(
                result
            )

        return results