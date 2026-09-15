from fastapi import APIRouter

from backend.app.services.traffic_service import (
    get_current_traffic
)

from backend.app.services.signal_service import (
    recommend_signal
)


router = APIRouter(
    prefix="/api/signals",
    tags=["Signals"]
)


@router.get("/recommendation")
def signal_recommendation():

    traffic_state = get_current_traffic()

    return recommend_signal(
        traffic_state
    )