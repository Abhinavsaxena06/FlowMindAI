from fastapi import APIRouter

from backend.app.services.prediction_service import (
    PredictionService
)


router = APIRouter(
    prefix="/api/prediction",
    tags=["Prediction"]
)


service = PredictionService()


@router.get("/")
def get_prediction():

    return service.predict()