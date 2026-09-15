class TrafficTrendAnalyzer:

    def __init__(self, history_size=20):

        self.history_size = history_size

        self.history = []

    def update(
        self,
        congestion_score
    ):

        self.history.append(
            congestion_score
        )

        if len(self.history) > self.history_size:

            self.history.pop(0)

    def get_trend(self):

        if len(self.history) < 3:

            return {
                "direction": "UNKNOWN",
                "change": 0.0
            }

        recent = self.history[-1]

        previous = self.history[-3]

        change = recent - previous

        if change > 5:

            direction = "INCREASING"

        elif change < -5:

            direction = "DECREASING"

        else:

            direction = "STABLE"

        return {
            "direction": direction,
            "change": round(
                change,
                2
            )
        }