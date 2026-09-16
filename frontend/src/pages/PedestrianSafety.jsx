import {
  AlertTriangle,
  CarFront,
  Clock3,
  Footprints,
  ShieldCheck,
  TimerReset,
  Users,
} from "lucide-react";

import useTrafficState from "../hooks/useTrafficState";
import usePedestrianSafety from "../hooks/usePedestrianSafety";

const stateColors = {
  WAIT: "warning",
  WALK: "success",
  COUNTDOWN: "warning",
  STOP: "danger",
  EMERGENCY: "danger",
  SAFE: "success",
  BLOCKED: "warning",
  CLEAR: "success",
};

export default function PedestrianSafety() {
  const { traffic } = useTrafficState();
  const vehicleSignal = traffic?.signalState || "UNKNOWN";
  const pedestrian = usePedestrianSafety(vehicleSignal);

  const vehicleState = String(vehicleSignal || "UNKNOWN").toUpperCase();
  const currentSignal = pedestrian.signalState || "WAIT";
  const queueState = pedestrian.requestPending
    ? "REQUESTED"
    : pedestrian.crossingActive
      ? "ACTIVE"
      : pedestrian.safetyStatus === "BLOCKED"
        ? "BLOCKED"
        : "READY";

  const safeToCross =
    pedestrian.requestPending &&
    vehicleState !== "GREEN" &&
    vehicleState !== "YELLOW";

  return (
    <div className="pedestrian-page">
      <header className="pedestrian-header">
        <div className="pedestrian-header-copy">
          <div className="eyebrow">PEDESTRIAN SAFETY</div>
          <h1 className="page-title">Pedestrian safety</h1>
          <p className="page-description">
            Zebra crossing coordination between pedestrian requests and the active traffic signal cycle.
          </p>
        </div>

        <div className="pedestrian-header-meta">
          <span className={`status-pill ${stateColors[currentSignal] || "warning"}`}>
            {currentSignal}
          </span>
          <span className={`status-pill ${stateColors[pedestrian.safetyStatus] || "success"}`}>
            {pedestrian.safetyStatus}
          </span>
        </div>
      </header>

      <div className="kpi-grid pedestrian-summary-grid">
        <div className="metric-card pedestrian-metric-card">
          <div className="metric-top">
            <div className="metric-label">Pedestrian safety status</div>
            <div className="metric-icon"><ShieldCheck size={17} /></div>
          </div>
          <div className="metric-value pedestrian-metric-value">
            <span>{pedestrian.safetyStatus}</span>
          </div>
          <div className="metric-change neutral">
            <AlertTriangle size={12} />
            {queueState}
          </div>
        </div>

        <div className="metric-card pedestrian-metric-card">
          <div className="metric-top">
            <div className="metric-label">Pedestrians waiting</div>
            <div className="metric-icon"><Users size={17} /></div>
          </div>
          <div className="metric-value pedestrian-metric-value">
            <span>{pedestrian.pedestriansWaiting}</span>
          </div>
          <div className="metric-change neutral">
            <Footprints size={12} />
            Waiting at crossing
          </div>
        </div>

        <div className="metric-card pedestrian-metric-card">
          <div className="metric-top">
            <div className="metric-label">Pedestrians crossing</div>
            <div className="metric-icon"><Footprints size={17} /></div>
          </div>
          <div className="metric-value pedestrian-metric-value">
            <span>{pedestrian.pedestriansCrossing}</span>
          </div>
          <div className="metric-change neutral">
            <Clock3 size={12} />
            {pedestrian.crossingActive ? "Crossing active" : "No active crossing"}
          </div>
        </div>

        <div className="metric-card pedestrian-metric-card">
          <div className="metric-top">
            <div className="metric-label">Vehicle signal</div>
            <div className="metric-icon"><CarFront size={17} /></div>
          </div>
          <div className="metric-value pedestrian-metric-value">
            <span>{vehicleState}</span>
          </div>
          <div className="metric-change neutral">
            <TimerReset size={12} />
            {pedestrian.countdown ? `${pedestrian.countdown}s remaining` : "Signal stable"}
          </div>
        </div>
      </div>

      <div className="pedestrian-layout">
        <div className="content-card pedestrian-stage-card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Zebra crossing</h2>
              <p className="card-subtitle">Pedestrian crossing coordination</p>
            </div>
          </div>

          <div className="card-body pedestrian-stage-body">
            <div className="pedestrian-stage">
              <div className="pedestrian-road pedestrian-road-horizontal" />
              <div className="pedestrian-road pedestrian-road-vertical" />

              <div className="zebra-crossing">
                <span />
                <span />
                <span />
                <span />
                <span />
                <span />
              </div>

              <div className="pedestrian-waiting-zone">
                <div className={`pedestrian-signal ${String(currentSignal).toLowerCase()}`}>
                  {currentSignal}
                </div>
              </div>

              <div className="vehicle-signal-box">
                <div className="signal-label">Vehicle</div>
                <div className={`vehicle-signal-light ${vehicleState.toLowerCase()}`}>
                  {vehicleState}
                </div>
              </div>

              <div className="pedestrian-direction-arrow">
                <span />
              </div>
            </div>
          </div>
        </div>

        <div className="content-card pedestrian-action-card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Crossing request</h2>
              <p className="card-subtitle">Operator or signal-controlled request</p>
            </div>
          </div>

          <div className="card-body action-body">
            <div className="pedestrian-request-row">
              <div>
                <div className="mini-label">Request status</div>
                <strong>{pedestrian.requestPending ? "PENDING" : pedestrian.crossingActive ? "ACTIVE" : "IDLE"}</strong>
              </div>

              <button
                type="button"
                className="primary-button pedestrian-request-button"
                onClick={pedestrian.requestCrossing}
                disabled={pedestrian.crossingActive || pedestrian.requestPending}
              >
                Request Crossing
              </button>
            </div>

            <div className="pedestrian-info-list">
              <div className="pedestrian-info-row">
                <span>Crossing signal</span>
                <strong>{currentSignal}</strong>
              </div>

              <div className="pedestrian-info-row">
                <span>Countdown</span>
                <strong>{pedestrian.countdown || 0}s</strong>
              </div>

              <div className="pedestrian-info-row">
                <span>Safety check</span>
                <strong>{safeToCross ? "SAFE" : vehicleState === "GREEN" ? "WAIT" : "READY"}</strong>
              </div>

              <div className="pedestrian-info-row">
                <span>Vehicle state</span>
                <strong>{vehicleState}</strong>
              </div>
            </div>

            <div className={`pedestrian-safety-banner ${stateColors[currentSignal] || "warning"}`}>
              {currentSignal === "WALK"
                ? "Pedestrians are currently allowed to cross."
                : currentSignal === "COUNTDOWN"
                  ? "Crossing time is actively counting down."
                  : currentSignal === "STOP"
                    ? "Pedestrian crossing is currently suspended."
                    : "Pedestrians must remain clear of the crossing until safe."}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
