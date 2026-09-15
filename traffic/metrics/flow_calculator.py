class FlowCalculator:

    def __init__(self):

        self.crossed_ids = set()

    def crossed_line(
        self,
        previous_point,
        current_point,
        line
    ):

        if (
            previous_point is None
            or
            current_point is None
            or
            line is None
        ):
            return False

        x1, y1 = line[0]
        x2, y2 = line[1]

        previous_side = (
            (x2 - x1)
            *
            (previous_point[1] - y1)
            -
            (y2 - y1)
            *
            (previous_point[0] - x1)
        )

        current_side = (
            (x2 - x1)
            *
            (current_point[1] - y1)
            -
            (y2 - y1)
            *
            (current_point[0] - x1)
        )

        return (
            previous_side * current_side
            < 0
        )

    def update(
        self,
        vehicle_id,
        previous_point,
        current_point,
        counting_line
    ):

        if vehicle_id in self.crossed_ids:
            return False

        crossed = self.crossed_line(
            previous_point,
            current_point,
            counting_line
        )

        if crossed:

            self.crossed_ids.add(
                vehicle_id
            )

            return True

        return False

    def count(
        self
    ):

        return len(
            self.crossed_ids
        )