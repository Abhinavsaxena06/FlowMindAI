from prediction.dataset import (
    load_states
)

from prediction.inference import (
    TrafficPredictor
)

from prediction.explainability import (
    explain_prediction
)


class PredictionService:

    def __init__(self):

        self.predictor = (
            TrafficPredictor()
        )

    def predict(self):

        states = load_states()

        if not states:

            return {
                "available": False,
                "message":
                    "No traffic history available."
            }

        result = self.predictor.predict(
            states
        )

        if not result.get(
            "available",
            False
        ):

            return result

        current = states[-1]

        predicted = result[
            "prediction"
        ]

        explanation = (
            explain_prediction(
                current,
                predicted
            )
        )

        return {

            "available": True,

            "horizon": {
                "short_term": "30 seconds",
                "long_term": "60 seconds"
            },

            "prediction":
                predicted,

            "explanation":
                explanation,

            "model":
                "FlowMind Traffic Transformer"
        }