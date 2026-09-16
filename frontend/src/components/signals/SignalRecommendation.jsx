import {
  ArrowRight,
  BrainCircuit,
} from "lucide-react";


export default function SignalRecommendation({
  recommendation = null,
  traffic = null,
}) {

  const strategy =
    recommendation?.recommended_strategy ||
    {};


  const phase =
    strategy.phase ||
    "waiting";


  const action =
    strategy.action ||
    "WAITING";


  const duration =
    Number(
      strategy.duration_seconds ||
      0
    );


  const metrics =
    recommendation?.metrics ||
    {};


  const explanation =
    traffic
      ? `FlowMind is using current traffic state and forecast data to evaluate signal strategies for Junction A.`
      : "Waiting for live traffic data from the perception engine.";


  return (
    <div className="recommendation-card">

      <div className="recommendation-icon">
        <BrainCircuit
          size={21}
        />
      </div>


      <div className="eyebrow">
        FLOWMIND RECOMMENDATION
      </div>


      <h2>
        {phase === "waiting"
          ? "Waiting for recommendation"
          : `Prioritize the ${phase.toUpperCase()} approach`}
      </h2>


      <p>
        {recommendation
          ? `Recommended action: ${action.replaceAll("_", " ")} for approximately ${duration} seconds.`
          : explanation}
      </p>


      <div className="recommendation-stats">

        <div>

          <strong>
            {duration || "—"}
          </strong>

          <span>
            green duration
          </span>

        </div>


        <div>

          <strong>
            {metrics.throughput ??
              "—"}
          </strong>

          <span>
            projected throughput
          </span>

        </div>


        <div>

          <strong>
            {metrics.average_waiting_time ??
              metrics.avg_waiting ??
              "—"}
          </strong>

          <span>
            projected waiting
          </span>

        </div>

      </div>


      <button className="primary-button">

        Review recommendation

        <ArrowRight
          size={16}
        />

      </button>

    </div>
  );
}