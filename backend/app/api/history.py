from fastapi import APIRouter

from backend.app.services.traffic_history_service import (
    TrafficHistoryService
)


router = APIRouter(
    prefix="/api/history",
    tags=["History"]
)


history_service = (
    TrafficHistoryService()
)


@router.get("/recent")
def recent_history(
    limit: int = 50
):

    return {
        "count": limit,

        "states":
            history_service.load_recent(
                limit
            )
    }