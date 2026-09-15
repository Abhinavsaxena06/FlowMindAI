import time


class TrafficForecast:

    def __init__(self, predictor):

        self.predictor = predictor

    def generate(
        self,
        horizon_seconds: int = 60,
    ):

        prediction = self.predictor.predict(
            horizon_seconds=horizon_seconds
        )

        return {
            "generated_at": time.time(),

            "horizon_seconds":
                horizon_seconds,

            "approaches":
                prediction,
        }