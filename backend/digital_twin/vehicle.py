class TwinVehicle:
    def __init__(
        self,
        vehicle_id,
        vehicle_type="car",
        approach="north",
        position=0.0,
        speed_kmh=0.0,
        desired_speed_kmh=35.0,
    ):
        self.id = vehicle_id
        self.vehicle_type = vehicle_type
        self.approach = approach

        # 0.0 = beginning of approach
        # 1.0 = completed junction crossing
        self.position = float(position)

        self.speed_kmh = float(speed_kmh)
        self.desired_speed_kmh = float(desired_speed_kmh)

        self.waiting_time = 0.0
        self.distance_travelled = 0.0
        self.completed = False

    # =========================================================
    # STATE HELPERS
    # =========================================================

    def is_stopped(self):
        return self.speed_kmh <= 1.0

    def is_moving(self):
        return self.speed_kmh > 5.0

    # =========================================================
    # UPDATE VEHICLE
    # =========================================================

    def update(self, green, seconds=1.0):
        if self.completed:
            return

        seconds = max(0.1, float(seconds))

        # -----------------------------------------------------
        # GREEN
        # -----------------------------------------------------

        if green:

            acceleration = 5.0

            if self.speed_kmh < self.desired_speed_kmh:

                self.speed_kmh += (
                    acceleration * seconds
                )

                if (
                    self.speed_kmh
                    > self.desired_speed_kmh
                ):
                    self.speed_kmh = (
                        self.desired_speed_kmh
                    )

        # -----------------------------------------------------
        # RED / ALL RED
        # -----------------------------------------------------

        else:

            deceleration = 10.0

            self.speed_kmh -= (
                deceleration * seconds
            )

            if self.speed_kmh < 0.0:
                self.speed_kmh = 0.0

        # -----------------------------------------------------
        # MOVEMENT
        # -----------------------------------------------------

        distance_m = (
            self.speed_kmh / 3.6
        ) * seconds

        # Simulated approach length = 150 m.
        position_change = (
            distance_m / 150.0
        )

        self.position += position_change

        # -----------------------------------------------------
        # WAITING TIME
        # -----------------------------------------------------

        if self.speed_kmh <= 1.0:

            self.waiting_time += seconds

        # -----------------------------------------------------
        # DISTANCE
        # -----------------------------------------------------

        self.distance_travelled += distance_m

        # -----------------------------------------------------
        # JUNCTION COMPLETION
        # -----------------------------------------------------

        if self.position >= 1.0:

            self.position = 1.0

            self.speed_kmh = (
                self.desired_speed_kmh
            )

            self.completed = True

    # =========================================================
    # SERIALIZATION
    # =========================================================

    def get_state(self):

        return {
            "id": self.id,
            "vehicle_type": self.vehicle_type,
            "approach": self.approach,
            "position": round(
                self.position,
                4
            ),
            "speed_kmh": round(
                self.speed_kmh,
                2
            ),
            "waiting_time": round(
                self.waiting_time,
                2
            ),
            "distance_travelled": round(
                self.distance_travelled,
                2
            ),
            "completed": self.completed,
        }