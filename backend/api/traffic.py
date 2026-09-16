import asyncio

import cv2

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from fastapi.responses import Response

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
# EXPLANATION
# ================================================================

@router.get("/explanation")
def get_traffic_explanation():

    result = (
        traffic_runtime
        .get_latest_result()
    )

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
# HISTORY
#
# Returns a flat time-series.
# This is what Overview + Network graphs need.
# ================================================================

@router.get("/history")
def get_history(limit: int = 30):

    limit = max(
        1,
        min(limit, 60)
    )

    engine = traffic_runtime.engine

    state_engine = (
        engine.traffic_engine.state_engine
    )

    states = (
        state_engine
        .get_recent_states()
    )

    states = states[-limit:]

    history = []

    for state in states:

        approaches = (
            state.get(
                "approaches",
                {}
            )
        )

        total_vehicles = 0
        total_queue = 0
        total_stopped = 0
        weighted_speed = 0
        density_total = 0

        lane_counts = {}

        for approach in [
            "north",
            "east",
            "south",
            "west",
        ]:

            data = approaches.get(
                approach,
                {}
            )

            vehicles = float(
                data.get(
                    "vehicles",
                    0
                )
            )

            queue = float(
                data.get(
                    "queue",
                    0
                )
            )

            stopped = float(
                data.get(
                    "stopped",
                    0
                )
            )

            speed = float(
                data.get(
                    "avg_speed_kmh",
                    0
                )
            )

            density = float(
                data.get(
                    "density",
                    0
                )
            )

            total_vehicles += vehicles
            total_queue += queue
            total_stopped += stopped

            weighted_speed += (
                vehicles * speed
            )

            density_total += density

            lane_counts[approach] = int(
                vehicles
            )

        average_speed = (
            weighted_speed / total_vehicles
            if total_vehicles > 0
            else 0
        )

        average_density = (
            density_total / 4
        )

        # Frontend-facing 0-100 congestion score.
        congestion_score = min(
            100,
            round(
                average_density * 45
                + min(total_queue / 20, 1.0) * 35
                + min(total_stopped / 20, 1.0) * 20
            )
        )

        history.append({
            "timestamp": state.get(
                "timestamp"
            ),

            "total_vehicles": int(
                total_vehicles
            ),

            "current_vehicles": int(
                total_vehicles
            ),

            "waiting_vehicles": int(
                total_queue
            ),

            "queue_count": int(
                total_queue
            ),

            "average_speed": round(
                average_speed,
                2
            ),

            "density": round(
                average_density,
                3
            ),

            "congestion_score": (
                congestion_score
            ),

            "lane_counts": lane_counts,

            "approaches": approaches,
        })

    return {
        "limit": limit,
        "count": len(history),
        "history": history,
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

                await websocket.send_json({
                    "status": "waiting"
                })

            else:

                await websocket.send_json(
                    result
                )

            await asyncio.sleep(1)

    except WebSocketDisconnect:

        pass

    except Exception:

        try:
            await websocket.close()
        except Exception:
            pass