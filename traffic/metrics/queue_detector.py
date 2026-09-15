class QueueDetector:

    def __init__(
        self,
        speed_threshold=8.0,
        queue_distance=100
    ):

        self.speed_threshold = speed_threshold

        self.queue_distance = queue_distance

    def distance_to_line(
        self,
        point,
        line
    ):

        if not line:
            return None

        x1, y1 = line[0]
        x2, y2 = line[1]

        x, y = point

        numerator = abs(
            (y2 - y1) * x
            -
            (x2 - x1) * y
            +
            x2 * y1
            -
            y2 * x1
        )

        denominator = (
            (
                (y2 - y1) ** 2
                +
                (x2 - x1) ** 2
            )
            ** 0.5
        )

        if denominator == 0:
            return None

        return numerator / denominator

    def is_queued(
        self,
        speed,
        point,
        stop_line=None
    ):

        if speed > self.speed_threshold:
            return False

        if stop_line is None:
            return True

        distance = self.distance_to_line(
            point,
            stop_line
        )

        if distance is None:
            return False

        return (
            distance
            <=
            self.queue_distance
        )

    def calculate(
        self,
        vehicles
    ):

        queue_count = 0

        for vehicle in vehicles:

            if vehicle.get(
                "queued",
                False
            ):
                queue_count += 1

        return queue_count