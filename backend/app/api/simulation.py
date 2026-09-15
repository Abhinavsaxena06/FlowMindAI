from fastapi import APIRouter, HTTPException

from backend.app.services.traffic_service import (
    get_current_traffic
)

from backend.app.services.simulation_service import (
    simulate_signal_strategy
)


router = APIRouter(
    prefix="/api/simulation",
    tags=["Simulation"]
)


@router.get("/compare")
def compare_strategies():

    traffic_state = get_current_traffic()

    results = []

    for strategy in [
        "FIXED",
        "ADAPTIVE",
        "PREDICTIVE"
    ]:

        results.append(
            simulate_signal_strategy(
                traffic_state,
                strategy
            )
        )

    return {
        "junction_id":
            traffic_state.get(
                "junction_id"
            ),

        "results": results
    }


@router.get("/{strategy}")
def run_strategy(
    strategy: str
):

    strategy = strategy.upper()

    if strategy not in [
        "FIXED",
        "ADAPTIVE",
        "PREDICTIVE"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Invalid strategy"
        )

    return simulate_signal_strategy(
        get_current_traffic(),
        strategy
    )