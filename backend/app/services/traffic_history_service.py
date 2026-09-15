import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class TrafficHistoryService:

    def __init__(self):
        self.history_file = Path(
            "data/traffic_states/latest_run.json"
        )

        self.history_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def _load_history(self) -> List[Dict[str, Any]]:
        if not self.history_file.exists():
            return []

        try:
            with open(
                self.history_file,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

            return []

        except (json.JSONDecodeError, OSError):
            return []

    def get_history(
        self,
        limit: int = 100
    ) -> List[Dict[str, Any]]:

        history = self._load_history()

        if limit <= 0:
            return []

        return history[-limit:]

    def get_latest(
        self
    ) -> Optional[Dict[str, Any]]:

        history = self._load_history()

        if not history:
            return None

        return history[-1]

    def get_summary(self) -> Dict[str, Any]:

        history = self._load_history()

        if not history:
            return {
                "total_records": 0,
                "average_vehicles": 0,
                "average_congestion": 0,
                "peak_vehicles": 0,
                "peak_congestion": 0
            }

        vehicle_values = []
        congestion_values = []

        for state in history:

            vehicles = state.get(
                "total_vehicles",
                0
            )

            congestion = state.get(
                "congestion_score",
                0
            )

            try:
                vehicle_values.append(
                    float(vehicles)
                )
            except (TypeError, ValueError):
                pass

            try:
                congestion_values.append(
                    float(congestion)
                )
            except (TypeError, ValueError):
                pass

        return {
            "total_records": len(history),

            "average_vehicles": (
                sum(vehicle_values) / len(vehicle_values)
                if vehicle_values
                else 0
            ),

            "average_congestion": (
                sum(congestion_values) / len(congestion_values)
                if congestion_values
                else 0
            ),

            "peak_vehicles": (
                max(vehicle_values)
                if vehicle_values
                else 0
            ),

            "peak_congestion": (
                max(congestion_values)
                if congestion_values
                else 0
            )
        }