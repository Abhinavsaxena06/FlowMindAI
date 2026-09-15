import { useEffect, useState } from "react";
import {
  BrainCircuit,
  TrendingUp,
  Gauge,
  Clock3,
  Activity,
  AlertTriangle,
} from "lucide-react";

import { getPrediction } from "../services/api";

export default function Predictions() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    async function load() {
      try {
        const result = await getPrediction();

        if (mounted) {
          setData(result);
        }
      } catch (error) {
        console.error("Prediction loading failed:", error);
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    load();

    return () => {
      mounted = false;
    };
  }, []);

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner" />
      </div>
    );
  }

  const prediction = data?.prediction || {};

  const available = Boolean(data && data.available !== false);

  const congestion = Number(
    prediction.congestion_score ??
      prediction.congestion ??
      0
  );

  const queue = Number(
    prediction.queue_count ??
      prediction.queue_length ??
      0
  );

  const speed = Number(
    prediction.average_speed ??
      prediction.avg_speed ??
      0
  );

  return (
    <div className="dashboard-grid">
      <div className="page-header">
        <div>
          <h1 className="page-title">Traffic Predictions</h1>

          <p className="page-description">
            Short-term traffic forecasting powered by the FlowMind
            prediction pipeline when data is available.
          </p>
        </div>

        <span className="status-pill demo-pill">
          <Activity size={12} />
          {available ? "AI Forecast" : "Collecting data"}
        </span>
      </div>

      {available ? (
        <>
          <div className="kpi-grid">
            <div className="metric-card">
              <div className="metric-top">
                <div className="metric-label">
                  Predicted Congestion
                </div>

                <div className="metric-icon">
                  <TrendingUp size={17} />
                </div>
              </div>

              <div className="metric-value">
                {congestion.toFixed(0)}
                <span className="metric-unit">/100</span>
              </div>

              <div className="metric-change negative">
                <AlertTriangle size={12} />
                Forecasted pressure
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-top">
                <div className="metric-label">
                  Predicted Queue
                </div>

                <div className="metric-icon">
                  <Gauge size={17} />
                </div>
              </div>

              <div className="metric-value">
                {queue.toFixed(0)}
                <span className="metric-unit">vehicles</span>
              </div>

              <div className="metric-change neutral">
                <Clock3 size={12} />
                Next 30 seconds
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-top">
                <div className="metric-label">
                  Predicted Speed
                </div>

                <div className="metric-icon">
                  <Gauge size={17} />
                </div>
              </div>

              <div className="metric-value">
                {speed.toFixed(1)}
                <span className="metric-unit">units</span>
              </div>

              <div className="metric-change positive">
                <TrendingUp size={12} />
                Network estimate
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-top">
                <div className="metric-label">
                  Model
                </div>

                <div className="metric-icon">
                  <BrainCircuit size={17} />
                </div>
              </div>

              <div className="metric-value">
                {data?.model || "FlowMind"}
              </div>

              <div className="metric-change neutral">
                {data?.horizon?.short_term || "Current horizon"}
              </div>
            </div>
          </div>

          <div className="two-column">
            <div className="content-card">
              <div className="card-header">
                <div>
                  <h2 className="card-title">
                    Forecast Overview
                  </h2>

                  <p className="card-subtitle">
                    Expected traffic state in the near future
                  </p>
                </div>
              </div>

              <div className="card-body">
                <div className="prediction-card">
                  <div className="prediction-header">
                    <div className="prediction-icon">
                      <BrainCircuit size={18} />
                    </div>

                    <div>
                      <div className="prediction-title">
                        FlowMind Prediction Engine
                      </div>

                      <div className="prediction-model">
                        Live model • 30–60 second horizon
                      </div>
                    </div>
                  </div>

                  <div className="prediction-main">
                    <div className="prediction-score">
                      {congestion.toFixed(0)}
                    </div>

                    <div className="prediction-label">
                      predicted congestion score
                    </div>
                  </div>

                  <p className="prediction-explanation">
                    {data?.explanation?.summary ||
                      "Traffic pressure is expected to change based on current traffic conditions."}
                  </p>

                  <div className="factor-list">
                    <span className="factor">
                      Vehicle volume
                    </span>

                    <span className="factor">
                      Queue growth
                    </span>

                    <span className="factor">
                      Average speed
                    </span>

                    <span className="factor">
                      Lane density
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="content-card">
              <div className="card-header">
                <div>
                  <h2 className="card-title">
                    Prediction Horizon
                  </h2>

                  <p className="card-subtitle">
                    Forecast windows
                  </p>
                </div>
              </div>

              <div className="card-body">
                <div className="alert-list">
                  <div className="alert-item">
                    <strong>Short term</strong>
                    <span>{data?.horizon?.short_term || "30 seconds"}</span>
                  </div>

                  <div className="alert-item">
                    <strong>Long term</strong>
                    <span>{data?.horizon?.long_term || "60 seconds"}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </>
      ) : (
        <div className="content-card">
          <div className="card-body">
            <div className="empty-chart">
              Prediction unavailable / collecting data.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}