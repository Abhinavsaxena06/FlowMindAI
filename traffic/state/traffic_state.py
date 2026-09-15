from datetime import datetime


class TrafficState:
    """
    Unified traffic state representation matching Section 25 specification.
    Provides structured telemetry for prediction, simulation, signal control, and dashboard.
    """

    def __init__(self, junction_id="JUNCTION-A"):
        self.junction_id = junction_id
        self.timestamp = datetime.now().isoformat()
        self.total_vehicles = 0
        self.vehicle_types = {}
        self.lanes = {
            "north": self._empty_lane(),
            "east": self._empty_lane(),
            "south": self._empty_lane(),
            "west": self._empty_lane()
        }
        self.overall_density = 0.0
        self.average_speed = 0.0
        self.total_queue = 0
        self.total_flow = 0.0
        self.average_waiting_time = 0.0
        self.signal_state = {
            "current_phase": "NORTH_SOUTH_GREEN",
            "phase_name": "North-South Green",
            "remaining_seconds": 25,
            "is_emergency": False,
            "active_strategy": "FLOWMIND_ADAPTIVE"
        }
        self.intersection_state = {
            "congestion_level": "LOW",
            "bottleneck_direction": "none",
            "active_incident": False
        }

    def _empty_lane(self):
        return {
            "vehicle_count": 0,
            "queue_length": 0,
            "density": 0.0,
            "average_speed": 0.0,
            "flow_rate": 0.0,
            "waiting_time": 0.0
        }

    def update(
        self,
        counts=None,
        queues=None,
        waiting_times=None,
        densities=None,
        speeds=None,
        flows=None,
        signal_state=None
    ):
        self.timestamp = datetime.now().isoformat()

        # Update vehicle counts
        if counts:
            self.total_vehicles = counts.get("total", 0)
            self.vehicle_types = counts.get("by_type", {})
            for lane, count in counts.get("by_lane", {}).items():
                if lane in self.lanes:
                    self.lanes[lane]["vehicle_count"] = count

        # Update queues
        if queues:
            total_q = 0
            for lane, q_len in queues.items():
                if lane in self.lanes:
                    self.lanes[lane]["queue_length"] = q_len
                    total_q += q_len
            self.total_queue = total_q

        # Update waiting times
        if waiting_times:
            by_lane_waits = waiting_times.get("by_lane", {})
            for lane, wait in by_lane_waits.items():
                if lane in self.lanes:
                    self.lanes[lane]["waiting_time"] = wait
            self.average_waiting_time = waiting_times.get("overall_average", 0.0)

        # Update densities
        if densities:
            for lane, dens in densities.get("by_lane", {}).items():
                if lane in self.lanes:
                    self.lanes[lane]["density"] = dens
            self.overall_density = densities.get("overall", 0.0)

        # Update speeds
        if speeds:
            for lane, spd in speeds.get("average_by_lane", {}).items():
                if lane in self.lanes:
                    self.lanes[lane]["average_speed"] = spd
            self.average_speed = speeds.get("overall_average", 0.0)

        # Update flows
        if flows:
            for lane, flw in flows.get("by_lane", {}).items():
                if lane in self.lanes:
                    self.lanes[lane]["flow_rate"] = flw
            self.total_flow = flows.get("overall", 0.0)

        # Update signal state
        if signal_state:
            self.signal_state.update(signal_state)

        # Determine congestion level
        if self.overall_density >= 0.75 or self.total_queue >= 20:
            self.intersection_state["congestion_level"] = "CRITICAL"
        elif self.overall_density >= 0.50 or self.total_queue >= 12:
            self.intersection_state["congestion_level"] = "HIGH"
        elif self.overall_density >= 0.30 or self.total_queue >= 6:
            self.intersection_state["congestion_level"] = "MODERATE"
        else:
            self.intersection_state["congestion_level"] = "LOW"

        # Determine bottleneck lane
        max_lane = max(self.lanes.keys(), key=lambda l: self.lanes[l]["queue_length"])
        if self.lanes[max_lane]["queue_length"] > 0:
            self.intersection_state["bottleneck_direction"] = max_lane
        else:
            self.intersection_state["bottleneck_direction"] = "none"

    def to_dict(self):
        return {
            "junction_id": self.junction_id,
            "timestamp": self.timestamp,
            "total_vehicles": self.total_vehicles,
            "vehicle_types": self.vehicle_types,
            "lanes": self.lanes,
            "overall_density": self.overall_density,
            "average_speed": self.average_speed,
            "total_queue": self.total_queue,
            "total_flow": self.total_flow,
            "average_waiting_time": self.average_waiting_time,
            "signal": self.signal_state,
            "intersection_state": self.intersection_state
        }