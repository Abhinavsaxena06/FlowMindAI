def explain_prediction(
    current,
    predicted
):

    explanations = []

    current_congestion = float(
        current.get(
            "congestion_score",
            0
        )
    )

    future_congestion = float(
        predicted.get(
            "congestion_score",
            current_congestion
        )
    )

    current_queue = float(
        current.get(
            "queue_count",
            0
        )
    )

    future_queue = float(
        predicted.get(
            "queue_count",
            current_queue
        )
    )

    current_speed = float(
        current.get(
            "average_speed",
            0
        )
    )

    future_speed = float(
        predicted.get(
            "average_speed",
            current_speed
        )
    )

    if (
        future_congestion
        >
        current_congestion + 0.05
    ):

        explanations.append(
            "Congestion is expected to increase."
        )

    if (
        future_queue
        >
        current_queue + 3
    ):

        explanations.append(
            "Vehicle queues are expected to grow."
        )

    if (
        future_speed
        <
        current_speed - 5
    ):

        explanations.append(
            "Average vehicle speed is expected to decrease."
        )

    if not explanations:

        explanations.append(
            "Traffic conditions are expected to remain relatively stable."
        )

    probability = min(
        0.99,
        max(
            0.01,
            abs(
                future_congestion
                -
                current_congestion
            )
            * 2
            +
            0.55
        )
    )

    return {
        "summary": explanations[0],
        "factors": explanations,
        "confidence": round(
            probability,
            2
        )
    }