from pydantic import BaseModel, Field
from typing import List


class PredictionPoint(BaseModel):

    horizon_seconds: int

    predicted_vehicle_count: float

    predicted_density: float = Field(
        ge=0,
        le=1
    )

    predicted_queue: float

    congestion_probability: float = Field(
        ge=0,
        le=1
    )


class TrafficPrediction(BaseModel):

    junction_id: str

    generated_at: str

    model: str

    confidence: float = Field(
        ge=0,
        le=1
    )

    predictions: List[PredictionPoint]

    explanation: str