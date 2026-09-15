import {
  BrainCircuit,
  ChevronRight,
} from "lucide-react";

export default function PredictionOverview({
  prediction,
}) {
  const data =
    prediction?.prediction || {};

  const congestion =
    Number(
      data.congestion_score ??
      data.congestion ??
      0
    );

  const message =
    prediction?.explanation?.summary ||
    "FlowMind is monitoring traffic patterns for near-term changes.";

  return (
    <div className="panel prediction-panel">

      <div className="prediction-icon">
        <BrainCircuit size={21} />
      </div>

      <div className="eyebrow">
        AI FORECAST
      </div>

      <h2>
        Next traffic condition
      </h2>

      <div className="prediction-score">
        {congestion.toFixed(0)}
        <span>%</span>
      </div>

      <p>
        {message}
      </p>

      <div className="prediction-bar">
        <span
          style={{
            width: `${Math.min(
              100,
              Math.max(
                0,
                congestion
              )
            )}%`,
          }}
        />
      </div>

      <div className="panel-footer-link">
        Open prediction center
        <ChevronRight size={15} />
      </div>

    </div>
  );
}