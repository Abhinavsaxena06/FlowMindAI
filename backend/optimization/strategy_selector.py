class StrategySelector:

    def calculate_score(self, result):

        metrics = result.get(
            "metrics",
            {}
        )

        waiting_time = float(
            metrics.get(
                "total_waiting_time",
                0
            )
        )

        stopped = float(
            metrics.get(
                "stopped_vehicles",
                0
            )
        )

        completed = float(
            metrics.get(
                "completed_vehicles",
                0
            )
        )

        distance = float(
            metrics.get(
                "total_distance",
                0
            )
        )

        throughput = float(
            metrics.get(
                "throughput",
                0
            )
        )

        # Lower score is better.
        #
        # Waiting and stopped vehicles are penalties.
        # Completed vehicles, distance and throughput
        # represent useful traffic movement.

        score = (
            waiting_time * 2.0
            + stopped * 5.0
            - completed * 10.0
            - distance * 0.05
            - throughput * 5.0
        )

        return round(
            score,
            2
        )

    def select(self, results):

        if not results:

            return {
                "recommended_strategy": None,
                "score": None,
                "metrics": {},
                "scenarios_tested": 0,
                "all_scenarios": [],
            }

        scored_results = []

        for result in results:

            score = (
                self.calculate_score(
                    result
                )
            )

            scored_results.append({
                "strategy": result[
                    "strategy"
                ],

                "metrics": result[
                    "metrics"
                ],

                "score": score,
            })

        scored_results.sort(
            key=lambda item: item["score"]
        )

        best = scored_results[0]

        return {
            "recommended_strategy": (
                best["strategy"]
            ),

            "score": best["score"],

            "metrics": best["metrics"],

            "scenarios_tested": len(
                scored_results
            ),

            "all_scenarios": (
                scored_results
            ),
        }