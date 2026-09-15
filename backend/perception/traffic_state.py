from collections import defaultdict, deque
from datetime import datetime, timezone
import math


class VehicleHistory:
    def __init__(self, max_points=30):
        self.positions = deque(maxlen=max_points)
        self.timestamps = deque(maxlen=max_points)

    def add(self, x, y, timestamp):
        self.positions.append((x, y))
        self.timestamps.append(timestamp)

    def speed_pixels_per_second(self):
        if len(self.positions) < 2:
            return 0.0

        x1, y1 = self.positions[-2]
        x2, y2 = self.positions[-1]

        t1 = self.timestamps[-2]
        t2 = self.timestamps[-1]

        dt = t2 - t1

        if dt <= 0:
            return 0.0

        distance = math.sqrt(
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2
        )

        return distance / dt


class TrafficStateEngine:

    def __init__(
        self,
        meters_per_pixel=0.04,
        queue_speed_kmh=8.0
    ):
        self.meters_per_pixel = meters_per_pixel
        self.queue_speed_kmh = queue_speed_kmh

        self.vehicle_history = {}

        self.state_history = deque(maxlen=60)

        self.total_seen_ids = set()

    def update_vehicle(
        self,
        vehicle_id,
        x,
        y,
        timestamp
    ):

        if vehicle_id not in self.vehicle_history:
            self.vehicle_history[vehicle_id] = VehicleHistory()

        self.vehicle_history[vehicle_id].add(
            x,
            y,
            timestamp
        )

        self.total_seen_ids.add(vehicle_id)

    def get_speed_kmh(self, vehicle_id):

        history = self.vehicle_history.get(vehicle_id)

        if history is None:
            return 0.0

        pixels_per_second = history.speed_pixels_per_second()

        meters_per_second = (
            pixels_per_second *
            self.meters_per_pixel
        )

        kmh = meters_per_second * 3.6

        return kmh

    def build_state(
        self,
        tracked_vehicles,
        timestamp=None
    ):

        if timestamp is None:
            timestamp = datetime.now(
                timezone.utc
            ).isoformat()

        approaches = {
            "north": [],
            "east": [],
            "south": [],
            "west": []
        }

        for vehicle in tracked_vehicles:

            vehicle_id = vehicle["id"]

            approach = vehicle.get(
                "approach"
            )

            if approach not in approaches:
                continue

            speed = self.get_speed_kmh(
                vehicle_id
            )

            approaches[approach].append({
                "id": vehicle_id,
                "class": vehicle["class"],
                "speed_kmh": round(speed, 2),
                "x": vehicle["x"],
                "y": vehicle["y"],
                "near_stop_line": vehicle.get(
                    "near_stop_line",
                    False
                )
            })

        state = {
            "junction": "JUNCTION-A",
            "timestamp": timestamp,
            "total_tracked_vehicles": len(
                tracked_vehicles
            ),
            "total_unique_vehicles": len(
                self.total_seen_ids
            ),
            "approaches": {}
        }

        for approach, vehicles in approaches.items():

            vehicle_count = len(vehicles)

            if vehicle_count > 0:

                average_speed = sum(
                    vehicle["speed_kmh"]
                    for vehicle in vehicles
                ) / vehicle_count

            else:
                average_speed = 0.0

            queue_count = sum(
                1
                for vehicle in vehicles
                if (
                    vehicle["speed_kmh"]
                    <= self.queue_speed_kmh
                    and vehicle["near_stop_line"]
                )
            )

            stopped_count = sum(
                1
                for vehicle in vehicles
                if vehicle["speed_kmh"] <= 5.0
            )

            density = self.calculate_density(
                vehicle_count
            )

            state["approaches"][approach] = {
                "vehicles": vehicle_count,
                "queue": queue_count,
                "stopped": stopped_count,
                "density": round(
                    density,
                    3
                ),
                "avg_speed_kmh": round(
                    average_speed,
                    2
                )
            }

        self.state_history.append(state)

        return state

    def calculate_density(
        self,
        vehicle_count
    ):

        # Temporary normalized density model.
        # This will later be replaced with
        # calibrated road occupancy.

        max_expected_vehicles = 25

        density = (
            vehicle_count /
            max_expected_vehicles
        )

        if density > 1.0:
            density = 1.0

        return density

    def get_recent_states(self):

        return list(
            self.state_history
        )