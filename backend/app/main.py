from fastapi import FastAPI

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
    traffic.router
)

app.include_router(
    history.router
)

app.include_router(
    prediction.router
)


@app.get("/")
def root():

    return {
        "name": "FlowMind",
        "status": "online",
        "message":
            "Predict Traffic. Optimize Signals. Move Cities Smarter."
    }