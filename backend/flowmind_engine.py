import time
import traceback


from backend.perception.live_traffic import LiveTrafficEngine

from backend.prediction.predictor import TrafficPredictor
from backend.prediction.forecast import TrafficForecast

from backend.optimization.scenario import ScenarioRunner
from backend.optimization.strategy_selector import StrategySelector
from backend.optimization.decision_explainer import (
    DecisionExplainer
)


class FlowMindEngine:
    """
    Main FlowMind orchestration engine.

    Pipeline:

        Video / Camera
             ↓
        YOLO + ByteTrack
             ↓
        Tracked Vehicles
             ↓
        Traffic State
             ↓
        Prediction
             ↓
        Forecast
             ↓
        Digital Twin
             ↓
        Strategy Selection
             ↓
        Traffic Recommendation
    """

    def __init__(
        self,
        state_interval_seconds=1.0,
        prediction_horizon_seconds=60,
    ):

        print()
        print("=" * 60)
        print("FLOWMIND ENGINE INITIALIZING")
        print("=" * 60)

        # =====================================================
        # CONFIGURATION
        # =====================================================

        self.state_interval_seconds = float(
            state_interval_seconds
        )

        self.prediction_horizon_seconds = int(
            prediction_horizon_seconds
        )

        # =====================================================
        # PERCEPTION
        # =====================================================

        print(
            "[FlowMind] Loading traffic perception engine..."
        )

        self.traffic_engine = LiveTrafficEngine()

        print(
            "[FlowMind] Traffic perception engine ready."
        )

        # =====================================================
        # PREDICTION
        # =====================================================

        print(
            "[FlowMind] Initializing prediction engine..."
        )

        self.predictor = TrafficPredictor()

        self.forecast_engine = TrafficForecast(
            self.predictor
        )

        print(
            "[FlowMind] Prediction engine ready."
        )

        # =====================================================
        # OPTIMIZATION
        # =====================================================

        print(
            "[FlowMind] Initializing optimization engine..."
        )

        self.strategy_selector = StrategySelector()
        self.decision_explainer = DecisionExplainer()

        print(
            "[FlowMind] Optimization engine ready."
        )

        # =====================================================
        # LATEST RESULTS
        # =====================================================

        self.latest_state = None

        self.latest_forecast = None

        self.latest_recommendation = None

        self.latest_result = None

        self.latest_frame = None

        # =====================================================
        # RUNTIME COUNTERS
        # =====================================================

        self.frames_processed = 0

        self.states_generated = 0

        self.last_state_timestamp = None

        self.last_error = None

        self.initialized = True

        print("=" * 60)
        print("FLOWMIND ENGINE READY")
        print("=" * 60)
        print()

    # =========================================================
    # PROCESS FRAME
    # =========================================================

    def process_frame(
        self,
        frame,
        timestamp=None,
    ):
        """
        Process one video/camera frame.

        LiveTrafficEngine.process_frame() returns:

            processed_frame
            tracked_vehicles
        """

        if timestamp is None:
            timestamp = time.time()

        try:

            # =================================================
            # STEP 1
            # YOLO + BYTE TRACK
            # =================================================

            (
                processed_frame,
                tracked_vehicles,
            ) = self.traffic_engine.process_frame(
                frame,
                timestamp,
            )

            self.frames_processed += 1

            self.latest_frame = processed_frame

            # =================================================
            # STEP 2
            # CHECK STATE INTERVAL
            # =================================================

            should_generate_state = False

            if self.last_state_timestamp is None:

                should_generate_state = True

            else:

                elapsed = (
                    timestamp
                    - self.last_state_timestamp
                )

                if (
                    elapsed
                    >= self.state_interval_seconds
                ):

                    should_generate_state = True

            # =================================================
            # RETURN LATEST DATA IF STATE IS NOT DUE
            # =================================================

            if not should_generate_state:

                return {
                    "frame":
                        processed_frame,

                    "tracked_vehicles":
                        tracked_vehicles,

                    "state":
                        self.latest_state,

                    "forecast":
                        self.latest_forecast,

                    "recommendation":
                        self.latest_recommendation,

                    "result":
                        self.latest_result,
                }

            # =================================================
            # STEP 3
            # BUILD TRAFFIC STATE
            # =================================================

            state_timestamp = (
                time.strftime(
                    "%Y-%m-%dT%H:%M:%SZ",
                    time.gmtime(timestamp),
                )
            )

            state = (
                self.traffic_engine
                .state_engine
                .build_state(
                    tracked_vehicles,
                    timestamp=state_timestamp,
                )
            )

            self.latest_state = state

            self.states_generated += 1

            self.last_state_timestamp = timestamp

            # =================================================
            # STEP 4
            # ADD STATE TO PREDICTOR
            # =================================================

            self.predictor.add_state(
                state,
                timestamp=timestamp,
            )

            # =================================================
            # STEP 5
            # GENERATE FORECAST
            # =================================================

            forecast = (
                self.forecast_engine.generate(
                    horizon_seconds=(
                        self.prediction_horizon_seconds
                    )
                )
            )

            self.latest_forecast = forecast

            # =================================================
            # STEP 6
            # OPTIMIZATION
            # =================================================

            recommendation = None

            result = None

            # -------------------------------------------------
            # IMPORTANT FIX
            # -------------------------------------------------
            #
            # TrafficForecast.generate() returns a dictionary
            # containing:
            #
            # {
            #     "generated_at": ...,
            #     "horizon_seconds": ...,
            #     "approaches": {...}
            # }
            #
            # It does NOT return:
            #
            # {
            #     "status": "ready"
            # }
            #
            # Therefore we determine readiness by checking
            # whether the forecast contains approach data.
            # -------------------------------------------------

            forecast_ready = (
                isinstance(
                    forecast,
                    dict,
                )
                and isinstance(
                    forecast.get(
                        "approaches"
                    ),
                    dict,
                )
                and len(
                    forecast.get(
                        "approaches",
                        {}
                    )
                ) > 0
            )

            # =================================================
            # RUN DIGITAL TWIN + STRATEGY SELECTION
            # =================================================

            if forecast_ready:

                try:

                    print(
                        "[FlowMind] Forecast ready."
                    )

                    # -----------------------------------------
                    # CREATE DIGITAL TWIN SCENARIO RUNNER
                    # -----------------------------------------

                    scenario_runner = (
                        ScenarioRunner(
                            traffic_state=state,
                            forecast=forecast,
                        )
                    )

                    # -----------------------------------------
                    # RUN ALL STRATEGIES
                    # -----------------------------------------

                    scenario_results = (
                        scenario_runner.run_all(
                            duration_seconds=60
                        )
                    )

                    # -----------------------------------------
                    # SELECT STRATEGY
                    # -----------------------------------------

                    recommendation = (
                        self.strategy_selector.select(
                            scenario_results
                        )
                    )

                    # -----------------------------------------
                    # SAVE COMPLETE RESULT
                    # -----------------------------------------

                    result = {
                        "scenarios":
                            scenario_results,

                        "recommendation":
                            recommendation,
                    }

                    print(
                        "[FlowMind] Recommendation generated."
                    )

                except Exception as optimization_error:

                    print()
                    print(
                        "[FlowMind] Optimization error:"
                    )

                    print(
                        optimization_error
                    )

                    traceback.print_exc()

                    result = {
                        "error":
                            str(
                                optimization_error
                            )
                    }

            # =================================================
            # FORECAST NOT READY
            # =================================================

            else:

                result = {
                    "status":
                        "warming_up",

                    "message":
                        "Waiting for usable traffic forecast.",

                    "forecast":
                        forecast,
                }

            # =================================================
            # STEP 7
            # SAVE RESULTS
            # =================================================

            self.latest_recommendation = (
                recommendation
            )

            explanation = self.decision_explainer.explain(
                traffic_state=state,
                forecast=forecast,
                recommendation=recommendation,
            )

            result = {
                "scenarios": scenario_results,
                "recommendation": recommendation,
                "explanation": explanation,
            }

            self.latest_result = result

            # =================================================
            # STEP 8
            # RETURN
            # =================================================

            return {
                "frame":
                    processed_frame,

                "tracked_vehicles":
                    tracked_vehicles,

                "state":
                    state,

                "forecast":
                    forecast,

                "recommendation":
                    recommendation,

                "result":
                    result,
            }

        except Exception as error:

            # =================================================
            # FRAME ERROR
            # =================================================

            self.last_error = str(error)

            print()
            print("=" * 60)
            print("FLOWMIND FRAME PROCESSING ERROR")
            print("=" * 60)
            print(error)
            print("=" * 60)

            traceback.print_exc()

            return {
                "frame":
                    self.latest_frame,

                "tracked_vehicles":
                    [],

                "state":
                    self.latest_state,

                "forecast":
                    self.latest_forecast,

                "recommendation":
                    self.latest_recommendation,

                "result":
                    self.latest_result,

                "error":
                    str(error),
            }

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):
        """
        Reset the current FlowMind runtime.

        The YOLO model itself is not reloaded.
        """

        print(
            "[FlowMind] Resetting engine..."
        )

        # -----------------------------------------------------
        # Latest results
        # -----------------------------------------------------

        self.latest_state = None

        self.latest_forecast = None

        self.latest_recommendation = None

        self.latest_result = None

        self.latest_frame = None

        # -----------------------------------------------------
        # Counters
        # -----------------------------------------------------

        self.frames_processed = 0

        self.states_generated = 0

        self.last_state_timestamp = None

        self.last_error = None

        # -----------------------------------------------------
        # Predictor history
        # -----------------------------------------------------

        if hasattr(
            self.predictor,
            "history",
        ):

            self.predictor.history.clear()

        # -----------------------------------------------------
        # Traffic state engine
        # -----------------------------------------------------

        if hasattr(
            self.traffic_engine,
            "state_engine",
        ):

            state_engine = (
                self.traffic_engine.state_engine
            )

            if hasattr(
                state_engine,
                "vehicle_history",
            ):

                state_engine.vehicle_history.clear()

            if hasattr(
                state_engine,
                "state_history",
            ):

                state_engine.state_history.clear()

            if hasattr(
                state_engine,
                "total_seen_ids",
            ):

                state_engine.total_seen_ids.clear()

        print(
            "[FlowMind] Engine reset complete."
        )

    # =========================================================
    # STANDARD GETTERS
    # =========================================================

    def get_state(self):

        return self.latest_state

    def get_forecast(self):

        return self.latest_forecast

    def get_recommendation(self):

        return self.latest_recommendation

    def get_result(self):

        return self.latest_result

    def get_frame(self):

        return self.latest_frame

    # =========================================================
    # COMPATIBILITY GETTERS
    # =========================================================
    #
    # traffic_runtime.py currently expects these names.
    #
    # We keep both naming styles so that the engine and runtime
    # remain compatible.
    # =========================================================

    def get_latest_state(self):

        return self.latest_state

    def get_latest_forecast(self):

        return self.latest_forecast

    def get_latest_recommendation(self):

        return self.latest_recommendation

    def get_latest_result(self):

        return self.latest_result

    def get_latest_frame(self):

        return self.latest_frame

    # =========================================================
    # STATUS
    # =========================================================

    def get_status(self):

        prediction_history = {}

        if hasattr(
            self.predictor,
            "history",
        ):

            prediction_history = {
                approach: len(history)
                for approach, history
                in self.predictor.history.items()
            }

        return {
            "initialized":
                self.initialized,

            "frames_processed":
                self.frames_processed,

            "states_generated":
                self.states_generated,

            "state_interval_seconds":
                self.state_interval_seconds,

            "prediction_horizon_seconds":
                self.prediction_horizon_seconds,

            "prediction_history":
                prediction_history,

            "has_state":
                self.latest_state is not None,

            "has_forecast":
                self.latest_forecast is not None,

            "has_recommendation":
                self.latest_recommendation is not None,

            "last_error":
                self.last_error,
        }