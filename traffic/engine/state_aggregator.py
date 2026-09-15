from datetime import datetime

from traffic.metrics.congestion_calculator import (
    calculate_congestion_score,
    get_traffic_status
)


class StateAggregator:

    def aggregate(
        self,
        junction_id: str,
        lanes: dict
    ):

        total_vehicles = sum(
            lane.get("vehicle_count", 0)
            for lane in lanes.values()
        )

        total_queue = sum(
            lane.get("queue_length", 0)
            for lane in lanes.values()
        )

        if lanes:

            average_speed = (
                sum(
                    lane.get(
                        "average_speed",
                        0
                    )
                    for lane in lanes.values()
                )
                / len(lanes)
            )

            overall_density = (
                sum(
                    lane.get(
                        "density",
                        0
                    )
                    for lane in lanes.values()
                )
                / len(lanes)
            )

        else:

            average_speed = 0

            overall_density = 0

        congestion_score = calculate_congestion_score(
            total_vehicles,
            total_queue,
            overall_density,
            average_speed
        )

        return {
            "junction_id": junction_id,
            "timestamp": datetime.now().isoformat(),

            "lanes": lanes,

            "total_vehicles": total_vehicles,

            "average_speed": round(
                average_speed,
                2
            ),

            "overall_density": round(
                overall_density,
                3
            ),

            "overall_queue": total_queue,

            "congestion_score": congestion_score,

            "traffic_status": get_traffic_status(
                congestion_score
            ),

            "processing_mode": "LIVE"
        }