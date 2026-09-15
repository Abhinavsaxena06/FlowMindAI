from traffic.lane.lane_mapper import LaneMapper
from traffic.lane.lane_config import LANES
from traffic.tracking.trajectory import TrajectoryTracker
from traffic.metrics.vehicle_counter import VehicleCounter
from traffic.metrics.queue_detector import QueueDetector
from traffic.metrics.density_calculator import DensityCalculator
from traffic.metrics.speed_estimator import SpeedEstimator
from traffic.metrics.flow_calculator import FlowCalculator
from traffic.state.traffic_state import TrafficState


class TrafficEngine:
    """
    Central traffic perception and state estimation engine.
    Orchestrates lane mapping, vehicle counting, trajectory tracking,
    queue detection, density calculation, calibrated speed estimation,
    and flow rate aggregation into a unified TrafficState.
    """

    def __init__(
        self,
        frame_width=1920,
        frame_height=1080,
        fps=30,
        junction_id="JUNCTION-A",
        lanes=None
    ):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.fps = fps
        self.junction_id = junction_id

        # Use configured lane polygons as default
        active_lanes = lanes if lanes is not None else LANES
        self.lane_mapper = LaneMapper(
            lanes=active_lanes,
            frame_width=self.frame_width,
            frame_height=self.frame_height
        )
        self.trajectory_tracker = TrajectoryTracker(max_history=30)
        self.vehicle_counter = VehicleCounter()
        self.queue_detector = QueueDetector(
            fps=self.fps,
            stationary_threshold=10.0,
            min_stationary_frames=12
        )
        self.density_calculator = DensityCalculator()
        self.speed_estimator = SpeedEstimator(meters_per_pixel=0.05)
        self.flow_calculator = FlowCalculator(window_seconds=60)

        self.state = TrafficState(junction_id=self.junction_id)

    def process(self, detections, current_signal=None):
        """
        Processes detections (raw or tracked) for a single frame.
        Assigns lanes, updates trajectories, and re-computes all state metrics.
        """
        # Assign lanes to all incoming detections
        vehicles = []
        for det in detections:
            vehicle = dict(det)
            vehicle["lane"] = self.lane_mapper.get_lane(det["bbox"])
            vehicles.append(vehicle)

        # Update trajectory tracking
        self.trajectory_tracker.update(vehicles)

        # Compute vehicle counts by lane and type
        counts = self.vehicle_counter.count(vehicles)

        # Detect queues and compute waiting times
        queue_candidates = self.queue_detector.update(
            vehicles,
            self.trajectory_tracker
        )
        queue_counts = self.queue_detector.count_by_lane(queue_candidates)
        waiting_times = self.queue_detector.get_waiting_times(queue_candidates)

        # Compute density per lane and overall
        densities = self.density_calculator.calculate(counts["by_lane"])

        # Compute calibrated vehicle and lane speeds
        speeds = self.speed_estimator.estimate(
            vehicles,
            self.trajectory_tracker,
            fps=self.fps
        )

        # Compute flow rate
        flows = self.flow_calculator.update(vehicles)

        # Update unified state
        self.state.update(
            counts=counts,
            queues=queue_counts,
            waiting_times=waiting_times,
            densities=densities,
            speeds=speeds,
            flows=flows,
            signal_state=current_signal
        )

        return self.state.to_dict()