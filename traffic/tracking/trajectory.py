from collections import defaultdict, deque
import math


class TrajectoryTracker:

    def __init__(
        self,
        max_history=30
    ):

        self.max_history = max_history

        self.history = defaultdict(
            lambda: deque(
                maxlen=max_history
            )
        )

    def update(
        self,
        tracks
    ):

        for track in tracks:

            track_id = track["track_id"]

            x1, y1, x2, y2 = track["bbox"]

            center_x = (
                x1 + x2
            ) / 2

            center_y = (
                y1 + y2
            ) / 2

            bottom_center = (
                center_x,
                y2
            )

            self.history[
                track_id
            ].append(
                bottom_center
            )

    def get(
        self,
        track_id
    ):

        return list(
            self.history.get(
                track_id,
                []
            )
        )

    def get_last(
        self,
        track_id
    ):

        points = self.get(
            track_id
        )

        if not points:
            return None

        return points[-1]

    def get_previous(
        self,
        track_id
    ):

        points = self.get(
            track_id
        )

        if len(points) < 2:
            return None

        return points[-2]

    def displacement(
        self,
        track_id
    ):

        points = self.get(
            track_id
        )

        if len(points) < 2:
            return 0.0

        p1 = points[-2]
        p2 = points[-1]

        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        return math.sqrt(
            dx * dx + dy * dy
        )

    def direction(
        self,
        track_id
    ):

        points = self.get(
            track_id
        )

        if len(points) < 5:
            return "unknown"

        first = points[-5]
        last = points[-1]

        dx = last[0] - first[0]
        dy = last[1] - first[1]

        if abs(dx) > abs(dy):

            if dx > 0:
                return "east"

            return "west"

        if dy > 0:
            return "south"

        return "north"