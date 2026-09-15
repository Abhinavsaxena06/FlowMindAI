from pathlib import Path

import numpy as np
import torch

from prediction.dataset import (
    FEATURE_NAMES,
    state_to_features
)

from prediction.model import (
    TrafficTransformer
)


class TrafficPredictor:

    def __init__(
        self,
        checkpoint_path=(
            "prediction/checkpoints/"
            "traffic_transformer.pt"
        )
    ):

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.model = TrafficTransformer()

        checkpoint = Path(
            checkpoint_path
        )

        self.loaded = False

        if checkpoint.exists():

            data = torch.load(
                checkpoint,
                map_location=self.device
            )

            self.model.load_state_dict(
                data[
                    "model_state_dict"
                ]
            )

            self.loaded = True

        self.model.to(
            self.device
        )

        self.model.eval()

    def normalize(
        self,
        values,
        minimum,
        maximum
    ):

        difference = (
            maximum
            -
            minimum
        )

        difference[
            difference == 0
        ] = 1.0

        return (
            values
            -
            minimum
        ) / difference

    def predict(
        self,
        states
    ):

        if not self.loaded:

            return {
                "available": False,
                "message":
                    "Transformer model not trained yet."
            }

        if len(states) < 20:

            return {
                "available": False,
                "message":
                    "At least 20 traffic states required."
            }

        features = np.array(
            [
                state_to_features(
                    state
                )
                for state in states[-20:]
            ],
            dtype=np.float32
        )

        minimum = features.min(
            axis=0
        )

        maximum = features.max(
            axis=0
        )

        normalized = self.normalize(
            features,
            minimum,
            maximum
        )

        x = torch.tensor(
            normalized,
            dtype=torch.float32
        ).unsqueeze(0)

        x = x.to(
            self.device
        )

        with torch.no_grad():

            output = self.model(
                x
            )

        predicted = (
            output.cpu()
            .numpy()[0]
        )

        predicted = (
            predicted
            *
            (
                maximum
                -
                minimum
            )
            +
            minimum
        )

        result = {}

        for i, name in enumerate(
            FEATURE_NAMES
        ):

            result[name] = round(
                float(
                    predicted[i]
                ),
                3
            )

        return {
            "available": True,
            "prediction": result
        }