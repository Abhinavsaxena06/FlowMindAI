import cv2
import numpy as np


class LaneMapper:
    """
    Maps vehicle positions to configured traffic lanes.

    Each lane polygon can be supplied as:
        [(x1, y1), (x2, y2), ...]

    OpenCV requires the polygon to be a NumPy array, so this
    class normalizes the format before using pointPolygonTest().
    """

    def __init__(self, lanes):
        self.lanes = lanes

        # Pre-convert all lane polygons once.
        self.polygons = {}

        for lane in self.lanes:
            polygon = np.array(
                lane.polygon,
                dtype=np.float32
            )

            # OpenCV expects Nx2 or Nx1x2 point format.
            polygon = polygon.reshape((-1, 1, 2))

            self.polygons[lane.lane_id] = polygon

    def point_inside_polygon(self, point, polygon):
        """
        Check whether a point lies inside a polygon.
        """

        x, y = point

        polygon = np.asarray(
            polygon,
            dtype=np.float32
        )

        polygon = polygon.reshape((-1, 1, 2))

        result = cv2.pointPolygonTest(
            polygon,
            (float(x), float(y)),
            False
        )

        return result >= 0

    def get_lane(self, point):
        """
        Return the lane containing the given point.

        Returns:
            lane_id string
            or None if the point is outside all lanes.
        """

        for lane in self.lanes:

            polygon = self.polygons[lane.lane_id]

            if self.point_inside_polygon(
                point,
                polygon
            ):
                return lane.lane_id

        return None

    def get_lane_object(self, point):
        """
        Return the complete Lane object containing the point.
        """

        for lane in self.lanes:

            polygon = self.polygons[lane.lane_id]

            if self.point_inside_polygon(
                point,
                polygon
            ):
                return lane

        return None

    def get_all_lanes(self):
        """
        Return all configured lanes.
        """

        return self.lanes

    def get_polygon(self, lane_id):
        """
        Return the OpenCV-compatible polygon for a lane.
        """

        return self.polygons.get(lane_id)