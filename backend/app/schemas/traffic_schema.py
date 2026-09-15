from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field


class LaneTraffic(BaseModel):

    lane_id: str

    vehicle_count: int = Field(
        default=0,
        ge=0
    )

    queue_length: int = Field(
        default=0,
        ge=0
    )

    density: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0
    )

    average_speed: float = Field(
        default=0.0,
        ge=0.0
    )

    flow: float = Field(
        default=0.0,
        ge=0.0
    )

    waiting_time: float = Field(
        default=0.0,
        ge=0.0
    )

    congestion_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0
    )


class TrafficState(BaseModel):

    junction_id: str

    timestamp: datetime

    lanes: Dict[str, LaneTraffic]

    total_vehicles: int = 0

    average_speed: float = 0.0

    overall_density: float = 0.0

    overall_queue: int = 0

    congestion_score: float = 0.0

    traffic_status: str = "LOW"

    processing_mode: str = "LIVE"