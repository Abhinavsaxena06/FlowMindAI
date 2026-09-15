from collections import Counter


class VehicleCounter:

    def count(self, tracked_objects):

        lane_counts = {
            "north": 0,
            "east": 0,
            "south": 0,
            "west": 0
        }

        vehicle_type_counts = Counter()

        for vehicle in tracked_objects:

            lane = vehicle.get("lane")

            vehicle_type = vehicle.get(
                "class_name",
                "unknown"
            )

            if lane in lane_counts:
                lane_counts[lane] += 1

            vehicle_type_counts[
                vehicle_type
            ] += 1

        return {
            "by_lane": lane_counts,
            "by_type": dict(vehicle_type_counts),
            "total": len(tracked_objects)
        }