from fastapi import APIRouter

from backend.app.services.traffic_service import (
    get_current_traffic,
    start_video_processing,
    pipeline_status
)


router = APIRouter(
    prefix="/api/traffic",
    tags=["Traffic"]
)


@router.get("/current")
def current_traffic():

    return get_current_traffic()


@router.post("/start")
def start_pipeline():

    return start_video_processing()


@router.get("/pipeline-status")
def get_pipeline_status():

    return pipeline_status()