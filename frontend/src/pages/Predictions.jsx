import { useEffect, useState } from "react";
import {
  BrainCircuit,
  Clock3,
  Gauge,
  RefreshCw,
  TrendingUp,
  TriangleAlert,
} from "lucide-react";

const API_URL = "http://127.0.0.1:8000/api/traffic/current";

export default function Prediction() {
  const [traffic, setTraffic] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [lastUpdated, setLastUpdated] = useState(null);

  const generatePrediction = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(API_URL);

      if (!response.ok) {
        throw new Error(
          `Backend returned ${response.status}`
        );
      }

      const current = await response.json();

      setTraffic(current);

      const lanes = Object.values(current?.lanes || {});

      if (lanes.length === 0) {
        throw new Error("No traffic lane data available.");
      }

      const density =
        lanes.reduce(
          (sum, lane) =>
            sum + Number(lane.density || 0),
          0
        ) / lanes.length;

      const queue = lanes.reduce(
        (sum, lane) =>
          sum + Number(lane.queue_length || 0),
        0
      );

      const speed =
        lanes.reduce(
          (sum, lane) =>
            sum + Number(lane.avg_speed || 0),
          0
        ) / lanes.length;

      const vehicles = lanes.reduce(
        (sum, lane) =>
          sum + Number(lane.vehicle_count || 0),
        0
      );

      /*
       * Current frontend forecasting baseline.
       *
       * This is intentionally kept separate from the UI so
       * it can later be replaced by the real Transformer +
       * GNN prediction service.
       */

      const pressure =
        density * 0.65 +
        Math.min(queue / 100, 1) * 0.25 +
        Math.min(vehicles / 150, 1) * 0.1;

      const growth30 = Math.min(
        0.2,
        Math.max(0.02, pressure * 0.16)
      );

      const growth60 = Math.min(
        0.35,
        Math.max(0.04, pressure * 0.27)
      );

      const density30 = Math.min(
        1,
        density + growth30
      );

      const density60 = Math.min(
        1,
        density + growth60
      );

      const queue30 = Math.round(
        queue * (1 + growth30)
      );

      const queue60 = Math.round(
        queue * (1 + growth60)
      );

      const speed30 = Math.max(
        0,
        speed * (1 - growth30 * 0.65)
      );

      const speed60 = Math.max(
        0,
        speed * (1 - growth60 * 0.65)
      );

      setPrediction({
        currentDensity: density,
        currentQueue: queue,
        currentSpeed: speed,

        density30,
        density60,

        queue30,
        queue60,

        speed30,
        speed60,

        currentVehicles: vehicles,

        status30: getTrafficStatus(
          density30,
          queue30
        ),

        status60: getTrafficStatus(
          density60,
          queue60
        ),
      });

      setLastUpdated(new Date());
    } catch (err) {
      console.error("Prediction error:", err);

      setError(
        "Unable to generate prediction. Make sure the FastAPI backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    generatePrediction();

    const interval = setInterval(
      generatePrediction,
      10000
    );

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="fm-page">
      {/* HEADER */}
      <div className="fm-page-header">
        <div>
          <div className="fm-eyebrow">
            <BrainCircuit size={15} />
            FORECAST ENGINE
          </div>

          <h1>Traffic Prediction</h1>

          <p>
            Estimate upcoming traffic conditions using
            the latest junction state.
          </p>
        </div>

        <button
          className="fm-button"
          onClick={generatePrediction}
          disabled={loading}
        >
          <RefreshCw
            size={16}
            className={loading ? "fm-spin" : ""}
          />

          {loading ? "Predicting..." : "Predict Again"}
        </button>
      </div>

      {/* ERROR */}
      {error && (
        <div className="fm-error">
          <TriangleAlert size={20} />

          <div>
            <strong>Prediction unavailable</strong>
            <p>{error}</p>
          </div>
        </div>
      )}

      {/* MAIN PREDICTION */}
      {prediction && (
        <>
          <section className="fm-prediction-hero">
            <div className="fm-prediction-icon">
              <BrainCircuit size={28} />
            </div>

            <div>
              <span className="fm-small-label">
                30-SECOND FORECAST
              </span>

              <h2>
                {prediction.status30}
              </h2>

              <p>
                Expected traffic condition at{" "}
                {traffic?.junction ||
                  "JUNCTION-A"}.
              </p>
            </div>

            {lastUpdated && (
              <div className="fm-prediction-time">
                <Clock3 size={15} />

                {lastUpdated.toLocaleTimeString()}
              </div>
            )}
          </section>

          {/* CURRENT VS PREDICTED */}
          <div className="fm-prediction-grid">
            <PredictionMetric
              icon={<Gauge size={21} />}
              title="Predicted Density"
              current={prediction.currentDensity}
              future={prediction.density30}
              format={(value) =>
                `${(value * 100).toFixed(0)}%`
              }
            />

            <PredictionMetric
              icon={<TrendingUp size={21} />}
              title="Predicted Queue"
              current={prediction.currentQueue}
              future={prediction.queue30}
              format={(value) =>
                `${Math.round(value)} vehicles`
              }
            />

            <PredictionMetric
              icon={<Clock3 size={21} />}
              title="Predicted Speed"
              current={prediction.currentSpeed}
              future={prediction.speed30}
              format={(value) =>
                `${value.toFixed(1)} km/h`
              }
            />
          </div>

          {/* HORIZON */}
          <section className="fm-card">
            <div className="fm-card-header">
              <div>
                <h2>Forecast Horizon</h2>

                <p>
                  Expected traffic progression from
                  the current state.
                </p>
              </div>
            </div>

            <div className="fm-horizon">
              <ForecastPoint
                label="NOW"
                status={getTrafficStatus(
                  prediction.currentDensity,
                  prediction.currentQueue
                )}
                density={prediction.currentDensity}
                queue={prediction.currentQueue}
              />

              <div className="fm-horizon-line" />

              <ForecastPoint
                label="+30 SEC"
                status={prediction.status30}
                density={prediction.density30}
                queue={prediction.queue30}
              />

              <div className="fm-horizon-line" />

              <ForecastPoint
                label="+60 SEC"
                status={prediction.status60}
                density={prediction.density60}
                queue={prediction.queue60}
              />
            </div>
          </section>

          {/* MODEL NOTE */}
          <section className="fm-info-card">
            <div className="fm-info-icon">
              <BrainCircuit size={20} />
            </div>

            <div>
              <strong>
                FlowMind Forecast Pipeline
              </strong>

              <p>
                The frontend is currently consuming
                the live traffic state and producing a
                short-term baseline forecast. This
                prediction layer is structured so it can
                be replaced by the planned Transformer +
                GNN model without changing the dashboard.
              </p>
            </div>
          </section>
        </>
      )}
    </div>
  );
}

function PredictionMetric({
  icon,
  title,
  current,
  future,
  format,
}) {
  return (
    <div className="fm-metric-card">
      <div className="fm-metric-icon">
        {icon}
      </div>

      <div className="fm-metric-content">
        <span>{title}</span>

        <strong>
          {format(future)}
        </strong>

        <p>
          Current: {format(current)}
        </p>
      </div>
    </div>
  );
}

function ForecastPoint({
  label,
  status,
  density,
  queue,
}) {
  return (
    <div className="fm-forecast-point">
      <span className="fm-small-label">
        {label}
      </span>

      <div
        className={`fm-forecast-status ${getStatusClass(
          status
        )}`}
      >
        {status}
      </div>

      <strong>
        {(density * 100).toFixed(0)}% density
      </strong>

      <span>
        {Math.round(queue)} vehicles queued
      </span>
    </div>
  );
}

function getTrafficStatus(density, queue) {
  if (density >= 0.8 || queue >= 70) {
    return "Critical";
  }

  if (density >= 0.6 || queue >= 40) {
    return "Heavy";
  }

  if (density >= 0.4) {
    return "Moderate";
  }

  return "Normal";
}

function getStatusClass(status) {
  if (status === "Critical") return "critical";
  if (status === "Heavy") return "heavy";
  if (status === "Moderate") return "moderate";

  return "normal";
}