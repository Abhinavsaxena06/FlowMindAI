def calculate_lane_priority(
    lane
):

    queue = lane.get(
        "queue_length",
        0
    )

    density = lane.get(
        "density",
        0
    )

    waiting = lane.get(
        "waiting_time",
        0
    )

    congestion = lane.get(
        "congestion_score",
        0
    )

    score = (

        queue * 0.35

        + density * 30 * 0.20

        + min(waiting / 60, 1) * 20 * 0.15

        + congestion * 0.30
    )

    return min(
        round(score, 2),
        100
    )


def recommend_signal(
    traffic_state
):

    lanes = traffic_state.get(
        "lanes",
        {}
    )

    if not lanes:

        return {
            "junction_id":
                traffic_state.get(
                    "junction_id",
                    "JUNCTION-A"
                ),

            "recommended_lane": "NONE",

            "current_phase": "UNKNOWN",

            "recommended_green_time": 30,

            "priority_score": 0,

            "reason":
                "Insufficient traffic data.",

            "confidence": 0,

            "safety_status": "SAFE"
        }

    priorities = {}

    for lane_id, lane in lanes.items():

        priorities[lane_id] = (
            calculate_lane_priority(
                lane
            )
        )

    best_lane = max(
        priorities,
        key=priorities.get
    )

    priority = priorities[
        best_lane
    ]

    green_time = 30

    if priority >= 80:

        green_time = 60

    elif priority >= 60:

        green_time = 50

    elif priority >= 40:

        green_time = 40

    trend = traffic_state.get(
        "trend",
        {}
    ).get(
        "direction",
        "UNKNOWN"
    )

    if trend == "INCREASING":

        green_time += 5

    green_time = min(
        green_time,
        90
    )

    reason = (
        f"{best_lane} has the highest "
        f"traffic priority score ({priority:.1f}). "
        f"Traffic trend is {trend.lower()}."
    )

    confidence = min(
        0.95,
        0.50 + priority / 200
    )

    return {

        "junction_id":
            traffic_state.get(
                "junction_id",
                "JUNCTION-A"
            ),

        "recommended_lane":
            best_lane,

        "current_phase":
            "ADAPTIVE",

        "recommended_green_time":
            green_time,

        "priority_score":
            priority,

        "reason":
            reason,

        "confidence":
            round(
                confidence,
                2
            ),

        "safety_status":
            "SAFE"
    }