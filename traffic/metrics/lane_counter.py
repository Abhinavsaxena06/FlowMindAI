from collections import Counter


class LaneCounter:

    def count(self, tracked_vehicles):

        lane_counts = Counter()
        vehicle_types = {}

        for vehicle in tracked_vehicles:

            lane = vehicle.get(
                "lane",
                "unknown"
            )

            class_name = vehicle.get(
                "class_name",
                "unknown"
            )

            if lane == "unknown":
                continue

            lane_counts[lane] += 1

            if lane not in vehicle_types:
                vehicle_types[lane] = Counter()

            vehicle_types[lane][class_name] += 1

        return {
            "lane_counts": dict(
                lane_counts
            ),

            "vehicle_types": {
                lane: dict(types)
                for lane, types
                in vehicle_types.items()
            }
        }