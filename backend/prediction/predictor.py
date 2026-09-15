from collections import defaultdict
from typing import Optional
import time


class TrafficPredictor:

    APPROACHES = [
        "north",
        "east",
        "south",
        "west",
    ]

    def __init__(
        self,
        history_size: int = 60,
    ):

        self.history_size = history_size

        # ---------------------------------------------------------
        # Historical traffic values
        # ---------------------------------------------------------

        self.history = defaultdict(list)

    # =============================================================
    # ADD STATE
    # =============================================================

    def add_state(
        self,
        state,
        timestamp: Optional[float] = None,
    ):

        if timestamp is None:
            timestamp = time.time()

        # Make sure timestamp is numeric.
        if isinstance(timestamp, str):

            try:
                # Handle ISO timestamps ending with Z.
                timestamp = timestamp.replace(
                    "Z",
                    "+00:00"
                )

                from datetime import datetime

                timestamp = datetime.fromisoformat(
                    timestamp
                ).timestamp()

            except Exception:
                timestamp = time.time()

        for approach in self.APPROACHES:

            data = state.get(
                "approaches",
                {}
            ).get(
                approach,
                {}
            )

            # -----------------------------------------------------
            # IMPORTANT:
            #
            # TrafficStateEngine produces:
            #
            # vehicles
            # queue
            # avg_speed_kmh
            #
            # These are the correct keys.
            # -----------------------------------------------------

            vehicles = float(
                data.get(
                    "vehicles",
                    0
                )
            )

            queue = float(
                data.get(
                    "queue",
                    0
                )
            )

            speed = float(
                data.get(
                    "avg_speed_kmh",
                    0
                )
            )

            self.history[approach].append(
                {
                    "timestamp": timestamp,
                    "vehicles": vehicles,
                    "queue": queue,
                    "speed": speed,
                }
            )

            # Keep only recent history.
            if len(self.history[approach]) > self.history_size:
                self.history[approach].pop(0)

    # =============================================================
    # TREND
    # =============================================================

    def calculate_trend(
        self,
        approach: str,
        metric: str,
    ):

        values = self.history.get(
            approach,
            []
        )

        if len(values) < 2:
            return 0.0

        first = values[0]
        last = values[-1]

        value_change = (
            last[metric]
            -
            first[metric]
        )

        time_change = (
            last["timestamp"]
            -
            first["timestamp"]
        )

        if time_change <= 0:
            return 0.0

        # Change per minute.
        trend_per_minute = (
            value_change
            /
            time_change
        ) * 60.0

        return trend_per_minute

    # =============================================================
    # APPROACH PREDICTION
    # =============================================================

    def predict_approach(
        self,
        approach: str,
        horizon_seconds: int = 60,
    ):

        history = self.history.get(
            approach,
            []
        )

        if not history:

            return {
                "current_vehicles": 0.0,
                "current_queue": 0.0,
                "current_speed_kmh": 0.0,
                "predicted_vehicles": 0.0,
                "predicted_queue": 0.0,
                "predicted_speed_kmh": 0.0,
                "vehicle_arrival_rate_per_minute": 0.0,
                "queue_change_per_minute": 0.0,
            }

        latest = history[-1]

        current_vehicles = latest["vehicles"]
        current_queue = latest["queue"]
        current_speed = latest["speed"]

        # ---------------------------------------------------------
        # Calculate trends
        # ---------------------------------------------------------

        vehicle_trend = self.calculate_trend(
            approach,
            "vehicles"
        )

        queue_trend = self.calculate_trend(
            approach,
            "queue"
        )

        speed_trend = self.calculate_trend(
            approach,
            "speed"
        )

        horizon_minutes = (
            horizon_seconds / 60.0
        )

        # ---------------------------------------------------------
        # Linear baseline prediction
        # ---------------------------------------------------------

        predicted_vehicles = (
            current_vehicles
            +
            vehicle_trend * horizon_minutes
        )

        predicted_queue = (
            current_queue
            +
            queue_trend * horizon_minutes
        )

        predicted_speed = (
            current_speed
            +
            speed_trend * horizon_minutes
        )

        # ---------------------------------------------------------
        # Prevent impossible values
        # ---------------------------------------------------------

        predicted_vehicles = max(
            0.0,
            predicted_vehicles
        )

        predicted_queue = max(
            0.0,
            predicted_queue
        )

        predicted_speed = max(
            0.0,
            predicted_speed
        )

        return {

            "current_vehicles":
                round(
                    current_vehicles,
                    2
                ),

            "current_queue":
                round(
                    current_queue,
                    2
                ),

            "current_speed_kmh":
                round(
                    current_speed,
                    2
                ),

            "predicted_vehicles":
                round(
                    predicted_vehicles,
                    2
                ),

            "predicted_queue":
                round(
                    predicted_queue,
                    2
                ),

            "predicted_speed_kmh":
                round(
                    predicted_speed,
                    2
                ),

            "vehicle_arrival_rate_per_minute":
                round(
                    max(
                        0.0,
                        vehicle_trend
                    ),
                    2
                ),

            "queue_change_per_minute":
                round(
                    queue_trend,
                    2
                ),
        }

    # =============================================================
    # FULL PREDICTION
    # =============================================================

    def predict(
        self,
        horizon_seconds: int = 60,
    ):

        result = {}

        for approach in self.APPROACHES:

            result[approach] = (
                self.predict_approach(
                    approach,
                    horizon_seconds
                )
            )

        return result