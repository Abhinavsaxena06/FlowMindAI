from collections import defaultdict


class TrafficEventDetector:

    def __init__(self):

        self.previous_speeds = {}

        self.stationary_frames = defaultdict(int)

    def update(
        self,
        vehicles
    ):

        events = []

        for vehicle in vehicles:

            vehicle_id = vehicle.get(
                "track_id"
            )

            speed = float(
                vehicle.get(
                    "speed",
                    0
                )
            )

            previous_speed = (
                self.previous_speeds.get(
                    vehicle_id,
                    speed
                )
            )

            if (
                previous_speed > 25
                and
                speed < 5
            ):

                events.append({
                    "type": "sudden_stop",
                    "track_id": vehicle_id
                })

            if speed < 2:

                self.stationary_frames[
                    vehicle_id
                ] += 1

            else:

                self.stationary_frames[
                    vehicle_id
                ] = 0

            if (
                self.stationary_frames[
                    vehicle_id
                ] > 90
            ):

                events.append({
                    "type": "long_stationary",
                    "track_id": vehicle_id
                })

            self.previous_speeds[
                vehicle_id
            ] = speed

        return events