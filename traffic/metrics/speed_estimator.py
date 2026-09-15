import math
import time


class SpeedEstimator:

    def __init__(
        self,
        meters_per_pixel=0.05,
        fps=30.0
    ):

        self.meters_per_pixel = (
            meters_per_pixel
        )

        self.fps = fps

    def estimate(
        self,
        previous_point,
        current_point
    ):

        if (
            previous_point is None
            or
            current_point is None
        ):
            return 0.0

        dx = (
            current_point[0]
            -
            previous_point[0]
        )

        dy = (
            current_point[1]
            -
            previous_point[1]
        )

        pixel_distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        meters = (
            pixel_distance
            *
            self.meters_per_pixel
        )

        seconds = 1.0 / self.fps

        meters_per_second = (
            meters / seconds
        )

        kmh = (
            meters_per_second
            *
            3.6
        )

        return round(
            kmh,
            2
        )

    def estimate_from_history(
        self,
        points
    ):

        if len(points) < 2:
            return 0.0

        total_distance = 0.0

        for i in range(
            1,
            len(points)
        ):

            x1, y1 = points[i - 1]
            x2, y2 = points[i]

            distance = math.sqrt(
                (x2 - x1) ** 2
                +
                (y2 - y1) ** 2
            )

            total_distance += distance

        meters = (
            total_distance
            *
            self.meters_per_pixel
        )

        seconds = (
            len(points) - 1
        ) / self.fps

        if seconds <= 0:
            return 0.0

        speed = (
            meters / seconds
        ) * 3.6

        return round(
            speed,
            2
        )