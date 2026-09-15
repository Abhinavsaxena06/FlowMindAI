class ZoneManager:

    def __init__(
        self,
        width: int,
        height: int
    ):

        self.width = width
        self.height = height

        self.zones = {
            "NORTH": {
                "x1": 0,
                "y1": 0,
                "x2": width,
                "y2": int(height * 0.35)
            },

            "SOUTH": {
                "x1": 0,
                "y1": int(height * 0.65),
                "x2": width,
                "y2": height
            },

            "WEST": {
                "x1": 0,
                "y1": int(height * 0.35),
                "x2": int(width * 0.35),
                "y2": int(height * 0.65)
            },

            "EAST": {
                "x1": int(width * 0.65),
                "y1": int(height * 0.35),
                "x2": width,
                "y2": int(height * 0.65)
            }
        }

    def get_zone(
        self,
        x: float,
        y: float
    ):

        for name, zone in self.zones.items():

            if (
                zone["x1"] <= x <= zone["x2"]
                and
                zone["y1"] <= y <= zone["y2"]
            ):

                return name

        return "INTERSECTION"

    def get_all_zones(self):

        return self.zones
    
    def classify(
        self,
        x: float,
        y: float
    ):

        return self.get_zone(
            x,
            y
        )