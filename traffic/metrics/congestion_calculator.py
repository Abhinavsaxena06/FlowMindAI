def calculate_congestion_score(
    vehicle_count,
    queue_length,
    density,
    average_speed,
    waiting_time=0
):

    vehicle_component = min(
        vehicle_count / 50,
        1
    ) * 15

    queue_component = min(
        queue_length / 30,
        1
    ) * 30

    density_component = min(
        density,
        1
    ) * 30

    speed_component = 0

    if average_speed <= 5:

        speed_component = 20

    elif average_speed <= 10:

        speed_component = 15

    elif average_speed <= 20:

        speed_component = 10

    elif average_speed <= 30:

        speed_component = 5

    waiting_component = min(
        waiting_time / 120,
        1
    ) * 5

    score = (
        vehicle_component
        + queue_component
        + density_component
        + speed_component
        + waiting_component
    )

    return round(
        min(score, 100),
        2
    )


def get_traffic_status(score):

    if score >= 85:
        return "CRITICAL"

    if score >= 65:
        return "SEVERE"

    if score >= 45:
        return "HIGH"

    if score >= 25:
        return "MODERATE"

    return "LOW"


def get_congestion_color(score):

    if score >= 85:
        return "CRITICAL"

    if score >= 65:
        return "SEVERE"

    if score >= 45:
        return "HIGH"

    if score >= 25:
        return "MODERATE"

    return "LOW"