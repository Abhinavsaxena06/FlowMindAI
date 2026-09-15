const results = [
  {
    label: "Average waiting",
    fixed: "48s",
    flowmind: "31s",
  },
  {
    label: "Queue length",
    fixed: "72",
    flowmind: "43",
  },
  {
    label: "Throughput",
    fixed: "812",
    flowmind: "934",
  },
  {
    label: "Congestion",
    fixed: "78%",
    flowmind: "54%",
  },
];

export default function SimulationResults() {
  return (
    <div className="panel">

      <div className="panel-header">

        <div>
          <div className="eyebrow">
            SIMULATION RESULT
          </div>

          <h2>
            Performance comparison
          </h2>
        </div>

      </div>

      <div className="result-table">

        <div className="result-row header">
          <span>Metric</span>
          <span>Fixed</span>
          <span>FlowMind</span>
        </div>

        {results.map(
          (result) => (
            <div
              className="result-row"
              key={result.label}
            >
              <span>
                {result.label}
              </span>

              <span>
                {result.fixed}
              </span>

              <strong>
                {result.flowmind}
              </strong>
            </div>
          )
        )}

      </div>

    </div>
  );
}