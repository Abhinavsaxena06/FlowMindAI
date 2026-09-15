from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from fastapi.responses import (
    Response,
)

from backend.services.traffic_runtime import (
    traffic_runtime,
)


router = APIRouter(
    prefix="/traffic",
    tags=["Traffic"],
)


# ================================================================
# STATUS
# ================================================================

@router.get("/status")
def get_status():

    return traffic_runtime.get_status()


# ================================================================
# START
# ================================================================

@router.post("/start")
def start_traffic(
    source: str = "data/videos/traffic.mp4",
):

    return traffic_runtime.start(
        source=source
    )


# ================================================================
# STOP
# ================================================================

@router.post("/stop")
def stop_traffic():

    return traffic_runtime.stop()


# ================================================================
# COMPLETE RESULT
# ================================================================

@router.get("/result")
def get_result():

    result = (
        traffic_runtime
        .get_latest_result()
    )

    if result is None:

        return {
            "status": "waiting",
            "message": (
                "FlowMind has not produced "
                "a traffic state yet."
            ),
        }

    return result


# ================================================================
# CURRENT TRAFFIC STATE
# ================================================================

@router.get("/state")
def get_state():

    state = (
        traffic_runtime
        .get_state()
    )

    if state is None:

        return {
            "status": "waiting"
        }

    return state


# ================================================================
# FORECAST
# ================================================================

@router.get("/forecast")
def get_forecast():

    forecast = (
        traffic_runtime
        .get_forecast()
    )

    if forecast is None:

        return {
            "status": "warming_up",
            "message": (
                "Waiting for enough "
                "traffic history."
            ),
        }

    return forecast


# ================================================================
# RECOMMENDATION
# ================================================================

@router.get("/recommendation")
def get_recommendation():

    recommendation = (
        traffic_runtime
        .get_recommendation()
    )

    if recommendation is None:

        return {
            "status": "warming_up",
            "message": (
                "Waiting for prediction "
                "before generating recommendation."
            ),
        }

    return recommendation


# ================================================================
# LATEST PROCESSED FRAME
# ================================================================

@router.get("/frame")
def get_frame():

    frame = (
        traffic_runtime
        .get_latest_frame()
    )

    if frame is None:

        return Response(
            content=b"",
            media_type="image/jpeg",
            status_code=404,
        )

    success, encoded = cv2.imencode(
        ".jpg",
        frame
    )

    if not success:

        return Response(
            content=b"",
            media_type="image/jpeg",
            status_code=500,
        )

    return Response(
        content=encoded.tobytes(),
        media_type="image/jpeg",
    )

# ================================================================
# TRAFFIC HISTORY
# ================================================================

@router.get("/history")
def get_history(limit: int = 30):

    limit = max(1, min(limit, 60))

    engine = traffic_runtime.engine

    history = {}

    for approach in engine.predictor.APPROACHES:

        values = engine.predictor.history.get(
            approach,
            []
        )

        values = values[-limit:]

        history[approach] = values

    return {
        "limit": limit,
        "count": max(
            [
                len(values)
                for values in history.values()
            ],
            default=0
        ),
        "approaches": history,
    }

@router.get("/traffic/explanation")
def get_traffic_explanation():

    result = traffic_runtime.get_latest_result()

    if not result:
        return {
            "status": "waiting",
            "explanation": None,
        }

    return {
        "status": "available",
        "explanation": result.get(
            "explanation"
        ),
    }
# ================================================================
# WEBSOCKET
# ================================================================

@router.websocket("/ws")
async def traffic_websocket(
    websocket: WebSocket,
):

    await websocket.accept()

    try:

        while True:

            result = (
                traffic_runtime
                .get_latest_result()
            )

            if result is None:

                await websocket.send_json(
                    {
                        "status": "waiting"
                    }
                )

            else:

                await websocket.send_json(
                    result
                )

            # Send approximately once per second.
            await asyncio.sleep(1)

    except WebSocketDisconnect:

        pass

    except Exception:

        try:
            await websocket.close()
        except Exception:
            pass