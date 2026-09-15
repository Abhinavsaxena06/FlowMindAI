from datetime import datetime


class WaitingTimeTracker:

    def __init__(
        self,
        stopped_speed=5
    ):

        self.stopped_speed = (
            stopped_speed
        )

        self.wait_start = {}

        self.total_wait = {}

    def update(
        self,
        vehicle_id,
        speed
    ):

        now = datetime.now()

        if speed <= self.stopped_speed:

            if vehicle_id not in self.wait_start:

                self.wait_start[
                    vehicle_id
                ] = now

        else:

            if vehicle_id in self.wait_start:

                start = self.wait_start.pop(
                    vehicle_id
                )

                elapsed = (
                    now - start
                ).total_seconds()

                self.total_wait[
                    vehicle_id
                ] = (
                    self.total_wait.get(
                        vehicle_id,
                        0
                    )
                    + elapsed
                )

    def get(
        self,
        vehicle_id
    ):

        total = self.total_wait.get(
            vehicle_id,
            0
        )

        if vehicle_id in self.wait_start:

            elapsed = (
                datetime.now()
                - self.wait_start[
                    vehicle_id
                ]
            ).total_seconds()

            total += elapsed

        return round(
            total,
            2
        )

    def get_all(self):

        return {
            vehicle_id:
                self.get(vehicle_id)

            for vehicle_id
            in set(
                list(
                    self.total_wait.keys()
                )
                +
                list(
                    self.wait_start.keys()
                )
            )
        }