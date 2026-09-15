from traffic.calibration.homography import (
    HomographyTransformer
)


image_points = [
    (100, 200),
    (500, 200),
    (500, 600),
    (100, 600)
]

world_points = [
    (0, 0),
    (20, 0),
    (20, 40),
    (0, 40)
]


transformer = HomographyTransformer(
    image_points,
    world_points
)


point = (
    300,
    400
)


result = transformer.transform_point(
    point
)


print(
    "Image point:",
    point
)

print(
    "World point:",
    result
)