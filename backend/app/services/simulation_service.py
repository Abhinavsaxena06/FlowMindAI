def simulate_signal_strategy(
    traffic_state: dict,
    strategy: str
):

    congestion = traffic_state.get(
        "congestion_score",
        0
    )

    queue = traffic_state.get(
        "overall_queue",
        0
    )

    if strategy == "FIXED":

        improvement = 0

    elif strategy == "ADAPTIVE":

        improvement = min(
            congestion * 0.18,
            30
        )

    elif strategy == "PREDICTIVE":

        improvement = min(
            congestion * 0.28,
            45
        )

    else:

        raise ValueError(
            "Unknown strategy"
        )

    predicted_congestion = max(
        congestion - improvement,
        0
    )

    predicted_queue = max(
        queue * (
            predicted_congestion
            / max(congestion, 1)
        ),
        0
    )

    return {

        "strategy": strategy,

        "baseline_congestion":
            round(congestion, 2),

        "predicted_congestion":
            round(
                predicted_congestion,
                2
            ),

        "baseline_queue":
            queue,

        "predicted_queue":
            round(
                predicted_queue,
                2
            ),

        "estimated_improvement":
            round(
                improvement,
                2
            )
    }