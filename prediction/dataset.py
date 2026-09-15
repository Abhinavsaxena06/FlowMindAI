from pathlib import Path
import json
import math
import random

import numpy as np
import torch
from torch.utils.data import Dataset


FEATURE_NAMES = [
    "total_vehicles",
    "queue_count",
    "average_speed",
    "density",
    "queue_ratio",
    "congestion_score",
    "north_count",
    "east_count",
    "south_count",
    "west_count"
]


def safe_float(value, default=0.0):

    try:
        value = float(value)

        if math.isnan(value):
            return default

        return value

    except (
        TypeError,
        ValueError
    ):
        return default


def state_to_features(state):

    lane_counts = state.get(
        "lane_counts",
        {}
    )

    return [
        safe_float(
            state.get(
                "total_vehicles",
                0
            )
        ),

        safe_float(
            state.get(
                "queue_count",
                0
            )
        ),

        safe_float(
            state.get(
                "average_speed",
                0
            )
        ),

        safe_float(
            state.get(
                "density",
                0
            )
        ),

        safe_float(
            state.get(
                "queue_ratio",
                0
            )
        ),

        safe_float(
            state.get(
                "congestion_score",
                0
            )
        ),

        safe_float(
            lane_counts.get(
                "north",
                0
            )
        ),

        safe_float(
            lane_counts.get(
                "east",
                0
            )
        ),

        safe_float(
            lane_counts.get(
                "south",
                0
            )
        ),

        safe_float(
            lane_counts.get(
                "west",
                0
            )
        )
    ]


def load_states(
    path="data/traffic_states/latest_run.json"
):

    file_path = Path(path)

    if not file_path.exists():

        return []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):

            return data

        return []

    except Exception:

        return []


def generate_demo_states(
    count=1000
):

    states = []

    base = 25.0

    for i in range(count):

        wave = math.sin(
            i / 35.0
        )

        noise = random.uniform(
            -3.0,
            3.0
        )

        vehicles = max(
            2,
            base
            +
            wave * 15
            +
            noise
        )

        queue = max(
            0,
            vehicles
            *
            random.uniform(
                0.15,
                0.55
            )
        )

        speed = max(
            5,
            55
            -
            queue * 1.1
            +
            random.uniform(
                -3,
                3
            )
        )

        density = min(
            1.0,
            vehicles / 50.0
        )

        queue_ratio = min(
            1.0,
            queue / vehicles
        )

        congestion = min(
            1.0,
            (
                density * 0.35
                +
                queue_ratio * 0.45
                +
                (
                    1
                    -
                    min(
                        speed / 60.0,
                        1.0
                    )
                )
                * 0.20
            )
        )

        north = max(
            0,
            int(
                vehicles
                *
                random.uniform(
                    0.20,
                    0.35
                )
            )
        )

        east = max(
            0,
            int(
                vehicles
                *
                random.uniform(
                    0.15,
                    0.30
                )
            )
        )

        south = max(
            0,
            int(
                vehicles
                *
                random.uniform(
                    0.20,
                    0.35
                )
            )
        )

        west = max(
            0,
            int(
                vehicles
                *
                random.uniform(
                    0.15,
                    0.30
                )
            )
        )

        states.append({

            "total_vehicles":
                round(
                    vehicles,
                    2
                ),

            "queue_count":
                round(
                    queue,
                    2
                ),

            "average_speed":
                round(
                    speed,
                    2
                ),

            "density":
                round(
                    density,
                    4
                ),

            "queue_ratio":
                round(
                    queue_ratio,
                    4
                ),

            "congestion_score":
                round(
                    congestion,
                    4
                ),

            "lane_counts": {

                "north": north,

                "east": east,

                "south": south,

                "west": west
            }
        })

    return states


class TrafficSequenceDataset(
    Dataset
):

    def __init__(
        self,
        states,
        sequence_length=20,
        prediction_horizon=1
    ):

        self.sequence_length = (
            sequence_length
        )

        self.prediction_horizon = (
            prediction_horizon
        )

        self.features = np.array(
            [
                state_to_features(
                    state
                )
                for state in states
            ],
            dtype=np.float32
        )

        self._normalize()

    def _normalize(self):

        self.minimum = (
            self.features.min(
                axis=0
            )
        )

        self.maximum = (
            self.features.max(
                axis=0
            )
        )

        difference = (
            self.maximum
            -
            self.minimum
        )

        difference[
            difference == 0
        ] = 1.0

        self.features = (
            (
                self.features
                -
                self.minimum
            )
            /
            difference
        )

    def __len__(self):

        return max(
            0,
            len(self.features)
            -
            self.sequence_length
            -
            self.prediction_horizon
            +
            1
        )

    def __getitem__(
        self,
        index
    ):

        end = (
            index
            +
            self.sequence_length
        )

        target_index = (
            end
            +
            self.prediction_horizon
            -
            1
        )

        x = self.features[
            index:end
        ]

        y = self.features[
            target_index
        ]

        return (
            torch.tensor(
                x,
                dtype=torch.float32
            ),
            torch.tensor(
                y,
                dtype=torch.float32
            )
        )