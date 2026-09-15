from traffic.tracking.trajectory import TrajectoryTracker
from traffic.lane.lane_mapper import LaneMapper

from traffic.metrics.speed_estimator import (
    SpeedEstimator
)

from traffic.metrics.queue_detector import (
    QueueDetector
)

from traffic.metrics.flow_calculator import (
    FlowCalculator
)

from traffic.metrics.traffic_events import (
    TrafficEventDetector
)


class TrafficEngine:

    def __init__(
        self,
        lanes,
        meters_per_pixel=0.05,
        fps=30.0
    ):

        self.lane_mapper = LaneMapper(
            lanes
        )

        self.trajectory_tracker = (
            TrajectoryTracker()
        )

        self.speed_estimator = (
            SpeedEstimator(
                meters_per_pixel,
                fps
            )
        )

        self.queue_detector = (
            QueueDetector()
        )

        self.flow_calculator = (
            FlowCalculator()
        )

        self.event_detector = (
            TrafficEventDetector()
        )

        self.frame_count = 0

    def process(
        self,
        tracks
    ):

        self.frame_count += 1

        self.trajectory_tracker.update(
            tracks
        )

        vehicles = []

        lane_counts = {}

        queue_count = 0

        total_speed = 0.0

        valid_speed_count = 0

        flow_events = 0

        for track in tracks:

            track_id = track[
                "track_id"
            ]

            bbox = track[
                "bbox"
            ]

            x1, y1, x2, y2 = bbox

            point = (
                (x1 + x2) / 2,
                y2
            )

            lane = (
                self.lane_mapper.get_lane(
                    point
                )
            )

            lane_id = None

            direction = "unknown"

            stop_line = None

            counting_line = None

            if lane:

                lane_id = lane.lane_id

                direction = lane.direction

                stop_line = lane.stop_line

                counting_line = (
                    lane.counting_line
                )

                lane_counts[
                    lane_id
                ] = (
                    lane_counts.get(
                        lane_id,
                        0
                    ) + 1
                )

            previous_point = (
                self.trajectory_tracker.get_previous(
                    track_id
                )
            )

            speed = (
                self.speed_estimator.estimate(
                    previous_point,
                    point
                )
            )

            queued = (
                self.queue_detector.is_queued(
                    speed,
                    point,
                    stop_line
                )
            )

            if queued:
                queue_count += 1

            if speed > 0:

                total_speed += speed

                valid_speed_count += 1

            crossed = (
                self.flow_calculator.update(
                    track_id,
                    previous_point,
                    point,
                    counting_line
                )
            )

            if crossed:
                flow_events += 1

            vehicle = {
                "track_id": track_id,
                "bbox": bbox,
                "class": track.get(
                    "class",
                    "vehicle"
                ),
                "confidence": track.get(
                    "confidence",
                    0.0
                ),
                "point": point,
                "lane": lane_id,
                "direction": direction,
                "speed": speed,
                "queued": queued
            }

            vehicles.append(
                vehicle
            )

        events = (
            self.event_detector.update(
                vehicles
            )
        )

        average_speed = 0.0

        if valid_speed_count > 0:

            average_speed = (
                total_speed
                /
                valid_speed_count
            )

        total_vehicles = len(
            vehicles
        )

        density = min(
            1.0,
            total_vehicles / 50.0
        )

        queue_ratio = 0.0

        if total_vehicles > 0:

            queue_ratio = (
                queue_count
                /
                total_vehicles
            )

        congestion_score = (
            (
                density * 0.35
            )
            +
            (
                queue_ratio * 0.45
            )
            +
            (
                max(
                    0.0,
                    1.0 -
                    average_speed / 60.0
                )
                * 0.20
            )
        )

        congestion_score = min(
            1.0,
            max(
                0.0,
                congestion_score
            )
        )

        if congestion_score < 0.25:
            traffic_status = "LOW"

        elif congestion_score < 0.50:
            traffic_status = "MODERATE"

        elif congestion_score < 0.75:
            traffic_status = "HIGH"

        else:
            traffic_status = "SEVERE"

        return {
            "frame": self.frame_count,

            "timestamp": (
                __import__(
                    "datetime"
                ).datetime.now().isoformat()
            ),

            "total_vehicles":
                total_vehicles,

            "lane_counts":
                lane_counts,

            "queue_count":
                queue_count,

            "average_speed":
                round(
                    average_speed,
                    2
                ),

            "density":
                round(
                    density,
                    3
                ),

            "queue_ratio":
                round(
                    queue_ratio,
                    3
                ),

            "flow_events":
                flow_events,

            "congestion_score":
                round(
                    congestion_score,
                    3
                ),

            "traffic_status":
                traffic_status,

            "vehicles":
                vehicles,

            "events":
                events
        }