import {
  AlertTriangle,
  ArrowUpRight,
  BrainCircuit,
} from "lucide-react";

export default function PredictionFactors({
  factors = [],
}) {
  const fallback = [
    {
      title:
        "North approach queue",
      detail:
        "Queue pressure is increasing.",
    },
    {
      title:
        "Average speed",
      detail:
        "Vehicle speeds are trending lower.",
    },
    {
      title:
        "Traffic density",
      detail:
        "Higher occupancy detected.",
    },
  ];

  const items =
    factors.length
      ? factors
      : fallback;

  return (
    <div className="panel">

      <div className="panel-header">

        <div>
          <div className="eyebrow">
            EXPLAINABLE AI
          </div>

          <h2>
            Why traffic may change
          </h2>
        </div>

        <BrainCircuit size={19} />

      </div>

      <div className="factor-list">

        {items.map(
          (factor, index) => (
            <div
              className="factor-row"
              key={index}
            >

              <div className="factor-number">
                0{index + 1}
              </div>

              <div className="factor-content">
                <strong>
                  {factor.title ||
                    factor.name}
                </strong>

                <span>
                  {factor.detail ||
                    factor.description}
                </span>
              </div>

              <ArrowUpRight
                size={16}
              />

            </div>
          )
        )}

      </div>

    </div>
  );
}