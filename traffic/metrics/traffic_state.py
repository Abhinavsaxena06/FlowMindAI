from datetime import datetime


class TrafficStateBuilder:

    def build(
        self,
        tracked_vehicles,
        lane_data,
        density_data,
        speed_data,
        queue_data,
        flow_data,
        waiting_time
    ):

        vehicle_types = {}

        for vehicle in tracked_vehicles:

            class_name = vehicle.get(
                "class_name",
                "unknown"
            )

            vehicle_types[class_name] = (
                vehicle_types.get(
                    class_name,
                    0
                ) + 1
            )

        return {
            "timestamp": datetime.now().isoformat(),

            "total_vehicles": len(
                tracked_vehicles
            ),

            "vehicle_types": vehicle_types,

            "lane_counts": lane_data.get(
                "lane_counts",
                {}
            ),

            "lane_vehicle_types": lane_data.get(
                "vehicle_types",
                {}
            ),

            "queue_lengths": queue_data,

            "density": density_data,

            "speed": speed_data,

            "flow": flow_data,

            "waiting_time": waiting_time
        }