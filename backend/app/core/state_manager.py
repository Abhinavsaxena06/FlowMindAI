from datetime import datetime
from threading import Lock
from typing import Any


class TrafficStateManager:

    def __init__(self):
        self._lock = Lock()

        self._state = {
            "junction_id": "JUNCTION-A",
            "timestamp": datetime.now().isoformat(),
            "status": "initializing",
            "lanes": {},
            "overall": {},
            "signal": {},
            "prediction": {},
            "network": {},
        }

    def update(self, state: dict[str, Any]):
        with self._lock:
            self._state = state.copy()

    def get_state(self):
        with self._lock:
            return self._state.copy()

    def update_section(
        self,
        section: str,
        data: dict[str, Any]
    ):
        with self._lock:
            self._state[section] = data
            self._state["timestamp"] = datetime.now().isoformat()

    def get_section(self, section: str):
        with self._lock:
            return self._state.get(
                section,
                {}
            )


traffic_state_manager = TrafficStateManager()