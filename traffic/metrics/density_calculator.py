class DensityCalculator:

    def __init__(
        self,
        maximum_vehicles=50
    ):

        self.maximum_vehicles = (
            maximum_vehicles
        )

    def calculate(
        self,
        vehicle_count
    ):

        if vehicle_count <= 0:
            return 0.0

        density = (
            vehicle_count
            / self.maximum_vehicles
        )

        return round(
            min(density, 1.0),
            3
        )

    def calculate_from_area(
        self,
        vehicle_count,
        area
    ):

        if area <= 0:
            return 0.0

        return round(
            vehicle_count / area,
            4
        )