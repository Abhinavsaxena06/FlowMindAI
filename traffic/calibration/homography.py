import cv2
import numpy as np


class HomographyTransformer:

    def __init__(
        self,
        image_points=None,
        world_points=None
    ):

        self.matrix = None

        if image_points is not None and world_points is not None:
            self.fit(
                image_points,
                world_points
            )

    def fit(
        self,
        image_points,
        world_points
    ):

        image_points = np.array(
            image_points,
            dtype=np.float32
        )

        world_points = np.array(
            world_points,
            dtype=np.float32
        )

        if len(image_points) < 4:
            raise ValueError(
                "At least 4 calibration points are required."
            )

        self.matrix, _ = cv2.findHomography(
            image_points,
            world_points
        )

        return self.matrix

    def transform_point(
        self,
        point
    ):

        if self.matrix is None:
            return point

        points = np.array(
            [[point]],
            dtype=np.float32
        )

        transformed = cv2.perspectiveTransform(
            points,
            self.matrix
        )

        x = float(transformed[0][0][0])
        y = float(transformed[0][0][1])

        return (
            x,
            y
        )

    def transform_points(
        self,
        points
    ):

        if self.matrix is None:
            return points

        points = np.array(
            [points],
            dtype=np.float32
        )

        transformed = cv2.perspectiveTransform(
            points,
            self.matrix
        )

        return transformed[0].tolist()