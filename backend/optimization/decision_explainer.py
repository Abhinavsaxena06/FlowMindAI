class DecisionExplainer:

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # MAIN EXPLANATION
    # ---------------------------------------------------------

    def explain(
        self,
        traffic_state,
        forecast,
        recommendation
    ):

        if not traffic_state or not recommendation:
            return self.empty_explanation()

        strategy = recommendation.get(
            "recommended_strategy",
            recommendation.get("strategy", {})
        )

        phase = strategy.get(
            "phase",
            "unknown"
        )

        action = strategy.get(
            "action",
            "HOLD_GREEN"
        )

        duration = strategy.get(
            "duration_seconds",
            10
        )

        current_approaches = traffic_state.get(
            "approaches",
            {}
        )

        forecast_approaches = {}

        if isinstance(forecast, dict):
            forecast_approaches = forecast.get(
                "approaches",
                {}
            )

        reasons = []

        current_pressure = 0.0
        predicted_pressure = 0.0

        # -----------------------------------------------------
        # ANALYZE CURRENT TRAFFIC
        # -----------------------------------------------------

        for approach, data in current_approaches.items():

            vehicles = self.to_float(
                data.get("vehicles", 0)
            )

            queue = self.to_float(
                data.get("queue", 0)
            )

            stopped = self.to_float(
                data.get("stopped", 0)
            )

            density = self.to_float(
                data.get("density", 0)
            )

            speed = self.to_float(
                data.get("avg_speed_kmh", 0)
            )

            pressure = (
                vehicles
                + queue * 2.0
                + stopped * 1.5
                + density * 10.0
            )

            current_pressure += pressure

            # Focus explanations on the recommended approach.

            if approach == phase:

                if queue >= 5:
                    reasons.append(
                        f"{approach.title()} has "
                        f"{int(queue)} queued vehicles."
                    )

                if stopped >= 3:
                    reasons.append(
                        f"{approach.title()} has "
                        f"{int(stopped)} stopped vehicles."
                    )

                if density >= 0.60:
                    reasons.append(
                        f"{approach.title()} has high "
                        f"traffic density ({density:.2f})."
                    )

                if speed > 0 and speed <= 10:
                    reasons.append(
                        f"{approach.title()} traffic is moving "
                        f"slowly at approximately {speed:.1f} km/h."
                    )

        # -----------------------------------------------------
        # ANALYZE FORECAST
        # -----------------------------------------------------

        forecast_data = forecast_approaches.get(
            phase,
            {}
        )

        predicted_vehicles = self.to_float(
            forecast_data.get(
                "predicted_vehicles",
                0
            )
        )

        predicted_queue = self.to_float(
            forecast_data.get(
                "predicted_queue",
                0
            )
        )

        predicted_speed = self.to_float(
            forecast_data.get(
                "predicted_avg_speed_kmh",
                0
            )
        )

        predicted_pressure = (
            predicted_vehicles
            + predicted_queue * 2.0
        )

        # -----------------------------------------------------
        # FORECAST REASONS
        # -----------------------------------------------------

        current_phase_data = current_approaches.get(
            phase,
            {}
        )

        current_queue = self.to_float(
            current_phase_data.get(
                "queue",
                0
            )
        )

        current_vehicles = self.to_float(
            current_phase_data.get(
                "vehicles",
                0
            )
        )

        if predicted_queue > current_queue + 2:
            reasons.append(
                f"Forecast indicates the {phase} queue "
                f"may increase from {int(current_queue)} "
                f"to approximately {int(predicted_queue)}."
            )

        if predicted_vehicles > current_vehicles + 2:
            reasons.append(
                f"Forecast indicates increasing vehicle "
                f"arrival pressure on the {phase} approach."
            )

        if predicted_speed > 0 and predicted_speed < 10:
            reasons.append(
                f"Predicted average speed on {phase} is "
                f"approximately {predicted_speed:.1f} km/h."
            )

        # -----------------------------------------------------
        # ARRIVAL RATE
        # -----------------------------------------------------

        arrival_rate = self.to_float(
            forecast_data.get(
                "arrival_rate",
                forecast_data.get(
                    "predicted_arrival_rate",
                    0
                )
            )
        )

        if arrival_rate > 0:
            reasons.append(
                f"Estimated arrival rate is "
                f"{arrival_rate:.2f} vehicles/minute."
            )

        # -----------------------------------------------------
        # DEFAULT REASON
        # -----------------------------------------------------

        if not reasons:
            reasons.append(
                f"Simulation found the {phase} phase "
                f"to be preferable under the current "
                f"traffic conditions."
            )

        # -----------------------------------------------------
        # EVIDENCE STRENGTH
        # -----------------------------------------------------

        evidence_count = len(reasons)

        if evidence_count >= 4:
            evidence_strength = "high"
        elif evidence_count >= 2:
            evidence_strength = "medium"
        else:
            evidence_strength = "low"

        # -----------------------------------------------------
        # HUMAN-READABLE SUMMARY
        # -----------------------------------------------------

        summary = (
            f"FlowMind recommends {action.replace('_', ' ').lower()} "
            f"for the {phase} approach for approximately "
            f"{int(duration)} seconds."
        )

        # -----------------------------------------------------
        # FINAL EXPLANATION OBJECT
        # -----------------------------------------------------

        return {

            "summary": summary,

            "recommended_phase": phase,

            "recommended_action": action,

            "recommended_duration_seconds": duration,

            "traffic_evidence": {
                "vehicles": current_vehicles,
                "queue": current_queue,
                "pressure": round(
                    current_pressure,
                    2
                )
            },

            "forecast_evidence": {
                "predicted_vehicles": predicted_vehicles,
                "predicted_queue": predicted_queue,
                "predicted_speed_kmh": predicted_speed,
                "arrival_rate": arrival_rate,
                "predicted_pressure": round(
                    predicted_pressure,
                    2
                )
            },

            "pressure": round(
                current_pressure,
                2
            ),

            "predicted_pressure": round(
                predicted_pressure,
                2
            ),

            "evidence_strength": evidence_strength,

            "reasons": reasons
        }

    # ---------------------------------------------------------
    # EMPTY RESULT
    # ---------------------------------------------------------

    def empty_explanation(self):

        return {

            "summary": (
                "FlowMind is waiting for enough "
                "traffic data to generate an explanation."
            ),

            "recommended_phase": None,

            "recommended_action": None,

            "recommended_duration_seconds": None,

            "traffic_evidence": {},

            "forecast_evidence": {},

            "pressure": 0.0,

            "predicted_pressure": 0.0,

            "evidence_strength": "low",

            "reasons": []
        }

    # ---------------------------------------------------------
    # SAFE NUMBER CONVERSION
    # ---------------------------------------------------------

    def to_float(self, value):

        try:
            return float(value)
        except (
            TypeError,
            ValueError
        ):
            return 0.0