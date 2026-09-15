from pydantic import BaseModel, Field


class SignalRecommendation(BaseModel):

    junction_id: str

    recommended_lane: str

    current_phase: str

    recommended_green_time: int = Field(
        ge=10,
        le=120
    )

    priority_score: float = Field(
        ge=0,
        le=100
    )

    reason: str

    confidence: float = Field(
        ge=0,
        le=1
    )

    safety_status: str = "SAFE"


class SignalStatus(BaseModel):

    junction_id: str

    current_phase: str

    remaining_seconds: int

    next_phase: str

    mode: str = "ADAPTIVE"

    emergency_override: bool = False