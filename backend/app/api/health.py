from fastapi import APIRouter

router = APIRouter(
    prefix="/api/health",
    tags=["Health"]
)


@router.get("")
def health_check():

    return {
        "status": "healthy",
        "service": "FlowMind Backend"
    }


@router.get("/ping")
def ping():

    return {
        "message":
            "FlowMind backend is running"
    }