from backend.api.traffic import router as traffic_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import (
    traffic,
    history,
    prediction
)


app = FastAPI(
    title="FlowMind API",
    description=(
        "Predictive Traffic Intelligence Platform"
    ),
    version="1.0.0"
)
app.include_router(
    traffic_router,
    prefix="/api"
)


app.include_router(
    traffic.router
)

app.include_router(
    history.router
)

app.include_router(
    prediction.router
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():

    return {
        "name": "FlowMind",
        "status": "online",
        "message":
            "Predict Traffic. Optimize Signals. Move Cities Smarter."
    }