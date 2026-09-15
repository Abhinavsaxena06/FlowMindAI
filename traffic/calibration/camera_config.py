from dataclasses import dataclass, field


@dataclass
class CameraConfig:

    camera_id: str = "JUNCTION-A"

    meters_per_pixel: float = 0.05

    fps: float = 30.0

    image_width: int = 1280

    image_height: int = 720

    calibration_image_points: list = field(
        default_factory=list
    )

    calibration_world_points: list = field(
        default_factory=list
    )

    def is_calibrated(self):

        return (
            len(self.calibration_image_points) >= 4
            and
            len(self.calibration_world_points) >= 4
        )