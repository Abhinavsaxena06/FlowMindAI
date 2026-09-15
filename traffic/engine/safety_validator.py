class SignalSafetyValidator:

    MIN_GREEN = 10

    MAX_GREEN = 90

    YELLOW_TIME = 3

    ALL_RED_TIME = 2

    def validate(
        self,
        recommendation
    ):

        green_time = recommendation.get(
            "recommended_green_time",
            30
        )

        if green_time < self.MIN_GREEN:

            green_time = self.MIN_GREEN

        if green_time > self.MAX_GREEN:

            green_time = self.MAX_GREEN

        recommendation[
            "recommended_green_time"
        ] = green_time

        recommendation[
            "safety_status"
        ] = "SAFE"

        recommendation[
            "transition"
        ] = {
            "yellow_seconds":
                self.YELLOW_TIME,

            "all_red_seconds":
                self.ALL_RED_TIME
        }

        return recommendation