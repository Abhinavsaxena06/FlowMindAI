import {
  ArrowRight,
  BrainCircuit,
} from "lucide-react";

export default function SignalRecommendation() {
  return (
    <div className="recommendation-card">

      <div className="recommendation-icon">
        <BrainCircuit size={21} />
      </div>

      <div className="eyebrow">
        FLOWMIND RECOMMENDATION
      </div>

      <h2>
        Prioritize the NORTH approach
      </h2>

      <p>
        North currently carries the highest
        queue pressure. Extending its green
        phase can reduce expected delay.
      </p>

      <div className="recommendation-stats">

        <div>
          <strong>
            −18%
          </strong>
          <span>
            expected queue
          </span>
        </div>

        <div>
          <strong>
            −11%
          </strong>
          <span>
            expected waiting
          </span>
        </div>

        <div>
          <strong>
            +9%
          </strong>
          <span>
            expected flow
          </span>
        </div>

      </div>

      <button className="primary-button">
        Review recommendation
        <ArrowRight size={16} />
      </button>

    </div>
  );
}