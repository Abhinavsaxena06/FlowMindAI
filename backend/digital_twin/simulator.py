from .vehicle import TwinVehicle
from .junction import TwinJunction


class DigitalTwinSimulator:

    STOP_LINE_POSITION = 0.72
    CLEAR_JUNCTION_POSITION = 0.80

    APPROACHES = [
        "north",
        "east",
        "south",
        "west",
    ]

    def __init__(
        self,
        traffic_state,
        forecast=None,
        signal_plan=None,
    ):

        self.original_state = (
            traffic_state or {}
        )

        self.forecast = (
            forecast or {}
        )

        self.signal_plan = (
            signal_plan or {}
        )

        self.simulation_time = 0.0

        self.vehicles = []

        self.completed_vehicles = []

        self.next_vehicle_id = 1

        self.arrival_accumulator = {
            approach: 0.0
            for approach in self.APPROACHES
        }

        # -----------------------------------------------------
        # Strategy statistics
        # -----------------------------------------------------

        self.completed_by_approach = {
            approach: 0
            for approach in self.APPROACHES
        }

        self.waiting_by_approach = {
            approach: 0.0
            for approach in self.APPROACHES
        }

        self.distance_by_approach = {
            approach: 0.0
            for approach in self.APPROACHES
        }

        # -----------------------------------------------------
        # Junction
        # -----------------------------------------------------

        self.junction = TwinJunction()

        # -----------------------------------------------------
        # Initial traffic
        # -----------------------------------------------------

        self.create_initial_vehicles()

        # -----------------------------------------------------
        # Apply signal strategy
        # -----------------------------------------------------

        self.configure_signal_plan()

    # =========================================================
    # SIGNAL PLAN
    # =========================================================

    def configure_signal_plan(self):

        phase = self.signal_plan.get(
            "phase",
            self.get_heaviest_approach()
        )

        if phase not in self.APPROACHES:
            phase = self.get_heaviest_approach()

        action = self.signal_plan.get(
            "action",
            "HOLD_GREEN"
        )

        try:

            duration = float(
                self.signal_plan.get(
                    "duration_seconds",
                    10
                )
            )

        except (
            TypeError,
            ValueError
        ):

            duration = 10.0

        duration = max(
            5.0,
            min(duration, 60.0)
        )

        # HOLD_GREEN keeps the normal 10 sec phase.
        if action == "HOLD_GREEN":
            duration = 10.0

        # EXTEND_GREEN uses the supplied duration.
        elif action == "EXTEND_GREEN":
            duration = duration

        else:
            duration = 10.0

        self.signal_plan = {
            "phase": phase,
            "action": action,
            "duration_seconds": int(
                duration
            ),
        }

        self.junction.configure_strategy(
            primary_phase=phase,
            primary_green_duration=duration,
            secondary_green_duration=10.0,
        )

    # =========================================================
    # HEAVIEST APPROACH
    # =========================================================

    def get_heaviest_approach(self):

        approaches = (
            self.original_state.get(
                "approaches",
                {}
            )
        )

        if not approaches:
            return "north"

        heaviest = "north"

        highest_pressure = -1.0

        for approach in self.APPROACHES:

            data = approaches.get(
                approach,
                {}
            )

            try:

                vehicles = float(
                    data.get(
                        "vehicles",
                        0
                    )
                )

            except (
                TypeError,
                ValueError
            ):

                vehicles = 0.0

            try:

                queue = float(
                    data.get(
                        "queue",
                        0
                    )
                )

            except (
                TypeError,
                ValueError
            ):

                queue = 0.0

            pressure = (
                vehicles
                + queue * 2.0
            )

            if pressure > highest_pressure:

                highest_pressure = pressure
                heaviest = approach

        return heaviest

    # =========================================================
    # INITIAL VEHICLES
    # =========================================================

    def create_initial_vehicles(self):

        approaches = (
            self.original_state.get(
                "approaches",
                {}
            )
        )

        for approach in self.APPROACHES:

            data = approaches.get(
                approach,
                {}
            )

            try:

                vehicle_count = int(
                    data.get(
                        "vehicles",
                        0
                    )
                )

            except (
                TypeError,
                ValueError
            ):

                vehicle_count = 0

            try:

                queue_count = int(
                    data.get(
                        "queue",
                        0
                    )
                )

            except (
                TypeError,
                ValueError
            ):

                queue_count = 0

            try:

                average_speed = float(
                    data.get(
                        "avg_speed_kmh",
                        20
                    )
                )

            except (
                TypeError,
                ValueError
            ):

                average_speed = 20.0

            queue_count = min(
                queue_count,
                vehicle_count
            )

            for index in range(
                vehicle_count
            ):

                # -------------------------------------------------
                # QUEUED VEHICLES
                # -------------------------------------------------

                if index < queue_count:

                    speed = 0.0

                    position = (
                        self.STOP_LINE_POSITION
                        - 0.035
                        - (index * 0.045)
                    )

                    position = max(
                        0.20,
                        position
                    )

                # -------------------------------------------------
                # MOVING VEHICLES
                # -------------------------------------------------

                else:

                    speed = max(
                        8.0,
                        average_speed
                    )

                    position = (
                        0.40
                        - (
                            (
                                index
                                - queue_count
                            )
                            * 0.045
                        )
                    )

                    position = max(
                        0.05,
                        position
                    )

                vehicle = TwinVehicle(
                    vehicle_id=self.next_vehicle_id,
                    vehicle_type="car",
                    approach=approach,
                    position=position,
                    speed_kmh=speed,
                    desired_speed_kmh=35.0,
                )

                self.next_vehicle_id += 1

                self.vehicles.append(
                    vehicle
                )

    # =========================================================
    # FORECAST ARRIVAL RATE
    # =========================================================

    def get_arrival_rate(
        self,
        approach
    ):

        forecast_approaches = (
            self.forecast.get(
                "approaches",
                {}
            )
        )

        data = forecast_approaches.get(
            approach,
            {}
        )

        value = data.get(
            "vehicle_arrival_rate_per_minute",
            0.0
        )

        try:

            return max(
                0.0,
                float(value)
            )

        except (
            TypeError,
            ValueError
        ):

            return 0.0

    # =========================================================
    # FUTURE ARRIVALS
    # =========================================================

    def add_future_arrivals(
        self,
        seconds=1.0
    ):

        for approach in self.APPROACHES:

            arrival_rate_per_minute = (
                self.get_arrival_rate(
                    approach
                )
            )

            arrival_rate_per_second = (
                arrival_rate_per_minute
                / 60.0
            )

            expected_arrivals = (
                arrival_rate_per_second
                * seconds
            )

            self.arrival_accumulator[
                approach
            ] += expected_arrivals

            while (
                self.arrival_accumulator[
                    approach
                ] >= 1.0
            ):

                self.arrival_accumulator[
                    approach
                ] -= 1.0

                self.create_arriving_vehicle(
                    approach
                )

    # =========================================================
    # CREATE ARRIVING VEHICLE
    # =========================================================

    def create_arriving_vehicle(
        self,
        approach
    ):

        vehicle = TwinVehicle(
            vehicle_id=self.next_vehicle_id,
            vehicle_type="car",
            approach=approach,
            position=0.02,
            speed_kmh=12.0,
            desired_speed_kmh=35.0,
        )

        self.next_vehicle_id += 1

        self.vehicles.append(
            vehicle
        )

    # =========================================================
    # STOP LINE
    # =========================================================

    def has_cleared_stop_line(
        self,
        vehicle
    ):

        return (
            vehicle.position
            >= self.CLEAR_JUNCTION_POSITION
        )

    # =========================================================
    # SIGNAL PERMISSION
    # =========================================================

    def can_vehicle_move(
        self,
        vehicle
    ):

        # -----------------------------------------------------
        # Once inside the junction, finish crossing.
        # -----------------------------------------------------

        if self.has_cleared_stop_line(
            vehicle
        ):

            return True

        # -----------------------------------------------------
        # Green
        # -----------------------------------------------------

        if self.junction.is_green(
            vehicle.approach
        ):

            return True

        # -----------------------------------------------------
        # Yellow
        #
        # Only vehicles already at the stop line
        # are allowed to continue.
        # -----------------------------------------------------

        if self.junction.is_yellow(
            vehicle.approach
        ):

            return (
                vehicle.position
                >= self.STOP_LINE_POSITION
            )

        # -----------------------------------------------------
        # ALL RED
        # -----------------------------------------------------

        return False

    # =========================================================
    # VEHICLE UPDATE
    # =========================================================

    def update_vehicles(
        self,
        seconds=1.0
    ):

        for vehicle in self.vehicles:

            if vehicle.completed:
                continue

            can_move = self.can_vehicle_move(
                vehicle
            )

            previous_position = (
                vehicle.position
            )

            vehicle.update(
                green=can_move,
                seconds=seconds
            )

            # -------------------------------------------------
            # Red-light protection
            # -------------------------------------------------

            if (
                not can_move
                and previous_position
                < self.STOP_LINE_POSITION
                and vehicle.position
                > self.STOP_LINE_POSITION
            ):

                vehicle.position = (
                    self.STOP_LINE_POSITION
                )

                vehicle.speed_kmh = 0.0

            # -------------------------------------------------
            # Completed vehicle
            # -------------------------------------------------

            if vehicle.completed:

                self.completed_vehicles.append(
                    vehicle
                )

                approach = (
                    vehicle.approach
                )

                self.completed_by_approach[
                    approach
                ] += 1

                self.waiting_by_approach[
                    approach
                ] += vehicle.waiting_time

                self.distance_by_approach[
                    approach
                ] += vehicle.distance_travelled

    # =========================================================
    # VEHICLE SPACING
    # =========================================================

    def apply_vehicle_spacing(self):

        minimum_gap = 0.040

        for approach in self.APPROACHES:

            approach_vehicles = [
                vehicle
                for vehicle in self.vehicles
                if (
                    vehicle.approach == approach
                    and not vehicle.completed
                )
            ]

            approach_vehicles.sort(
                key=lambda vehicle:
                vehicle.position,
                reverse=True
            )

            for index in range(
                1,
                len(approach_vehicles)
            ):

                front_vehicle = (
                    approach_vehicles[
                        index - 1
                    ]
                )

                current_vehicle = (
                    approach_vehicles[
                        index
                    ]
                )

                maximum_position = (
                    front_vehicle.position
                    - minimum_gap
                )

                if (
                    current_vehicle.position
                    > maximum_position
                ):

                    current_vehicle.position = (
                        maximum_position
                    )

                    if (
                        current_vehicle.position
                        < 0.0
                    ):

                        current_vehicle.position = 0.0

                    current_vehicle.speed_kmh = 0.0

    # =========================================================
    # REMOVE COMPLETED
    # =========================================================

    def remove_completed_vehicles(self):

        self.vehicles = [
            vehicle
            for vehicle in self.vehicles
            if not vehicle.completed
        ]

    # =========================================================
    # SIMULATION STEP
    # =========================================================

    def step(
        self,
        seconds=1.0
    ):

        # 1. New vehicles arrive.
        self.add_future_arrivals(
            seconds
        )

        # 2. Existing vehicles react to signal.
        self.update_vehicles(
            seconds
        )

        # 3. Maintain vehicle spacing.
        self.apply_vehicle_spacing()

        # 4. Advance signal.
        self.junction.advance(
            seconds
        )

        # 5. Advance simulation time.
        self.simulation_time += seconds

        # 6. Remove completed vehicles.
        self.remove_completed_vehicles()

    # =========================================================
    # RUN
    # =========================================================

    def run(
        self,
        duration_seconds=60
    ):

        duration_seconds = max(
            1,
            int(duration_seconds)
        )

        for _ in range(
            duration_seconds
        ):

            self.step(
                seconds=1.0
            )

        return self.get_metrics()

    # =========================================================
    # METRICS
    # =========================================================

    def get_metrics(self):

        active_vehicles = [
            vehicle
            for vehicle in self.vehicles
            if not vehicle.completed
        ]

        all_vehicles = (
            active_vehicles
            + self.completed_vehicles
        )

        moving_vehicles = sum(
            1
            for vehicle in active_vehicles
            if vehicle.speed_kmh > 5.0
        )

        stopped_vehicles = sum(
            1
            for vehicle in active_vehicles
            if vehicle.speed_kmh <= 1.0
        )

        total_waiting_time = sum(
            vehicle.waiting_time
            for vehicle in all_vehicles
        )

        total_distance = sum(
            vehicle.distance_travelled
            for vehicle in all_vehicles
        )

        # -----------------------------------------------------
        # Initial vehicles
        # -----------------------------------------------------

        initial_vehicles = 0

        for data in (
            self.original_state
            .get(
                "approaches",
                {}
            )
            .values()
        ):

            try:

                initial_vehicles += int(
                    data.get(
                        "vehicles",
                        0
                    )
                )

            except (
                TypeError,
                ValueError
            ):

                pass

        total_processed = len(
            all_vehicles
        )

        average_waiting_time = (
            total_waiting_time
            / max(
                1,
                total_processed
            )
        )

        throughput = (
            len(
                self.completed_vehicles
            )
            / max(
                1.0,
                self.simulation_time
            )
            * 60.0
        )

        # -----------------------------------------------------
        # Approach-level metrics
        # -----------------------------------------------------

        approach_metrics = {}

        for approach in self.APPROACHES:

            active_for_approach = [
                vehicle
                for vehicle in active_vehicles
                if vehicle.approach == approach
            ]

            approach_stopped = sum(
                1
                for vehicle in active_for_approach
                if vehicle.speed_kmh <= 1.0
            )

            approach_waiting = (
                self.waiting_by_approach[
                    approach
                ]
                + sum(
                    vehicle.waiting_time
                    for vehicle in active_for_approach
                )
            )

            approach_distance = (
                self.distance_by_approach[
                    approach
                ]
                + sum(
                    vehicle.distance_travelled
                    for vehicle in active_for_approach
                )
            )

            approach_metrics[
                approach
            ] = {

                "completed": (
                    self.completed_by_approach[
                        approach
                    ]
                ),

                "active": len(
                    active_for_approach
                ),

                "stopped": (
                    approach_stopped
                ),

                "waiting_time": round(
                    approach_waiting,
                    2
                ),

                "distance": round(
                    approach_distance,
                    2
                ),
            }

        # -----------------------------------------------------
        # Final result
        # -----------------------------------------------------

        return {

            "simulation_time_seconds": round(
                self.simulation_time,
                2
            ),

            "initial_vehicles": (
                initial_vehicles
            ),

            "total_vehicles_simulated": (
                total_processed
            ),

            "active_vehicles": (
                len(active_vehicles)
            ),

            "completed_vehicles": (
                len(
                    self.completed_vehicles
                )
            ),

            "moving_vehicles": (
                moving_vehicles
            ),

            "stopped_vehicles": (
                stopped_vehicles
            ),

            "total_waiting_time": round(
                total_waiting_time,
                2
            ),

            "total_distance": round(
                total_distance,
                2
            ),

            "average_waiting_time": round(
                average_waiting_time,
                2
            ),

            "throughput": round(
                throughput,
                2
            ),

            "active_queue": (
                stopped_vehicles
            ),

            "signal_phase": (
                self.junction.current_phase
            ),

            "signal_state": (
                self.junction.signal_state
            ),

            "primary_phase": (
                self.junction.primary_phase
            ),

            "primary_green_duration": round(
                self.junction.primary_green_duration,
                2
            ),

            "strategy": {
                "phase": self.signal_plan.get(
                    "phase"
                ),

                "action": self.signal_plan.get(
                    "action"
                ),

                "duration_seconds": self.signal_plan.get(
                    "duration_seconds"
                ),
            },

            "approaches": approach_metrics,
        }

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.simulation_time = 0.0

        self.vehicles = []

        self.completed_vehicles = []

        self.next_vehicle_id = 1

        self.arrival_accumulator = {
            approach: 0.0
            for approach in self.APPROACHES
        }

        self.completed_by_approach = {
            approach: 0
            for approach in self.APPROACHES
        }

        self.waiting_by_approach = {
            approach: 0.0
            for approach in self.APPROACHES
        }

        self.distance_by_approach = {
            approach: 0.0
            for approach in self.APPROACHES
        }

        self.junction = TwinJunction()

        self.create_initial_vehicles()

        self.configure_signal_plan()