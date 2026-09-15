import {
  Play,
  RotateCcw,
} from "lucide-react";

export default function SimulationControls({
  strategy,
  setStrategy,
  onRun,
  running,
}) {
  return (
    <div className="panel">

      <div className="panel-header">

        <div>
          <div className="eyebrow">
            DIGITAL TWIN
          </div>

          <h2>
            Scenario controls
          </h2>
        </div>

      </div>

      <label className="control-label">
        Signal strategy
      </label>

      <select
        className="control-select"
        value={strategy}
        onChange={(event) =>
          setStrategy(
            event.target.value
          )
        }
      >
        <option value="fixed">
          Fixed-time
        </option>

        <option value="adaptive">
          Adaptive
        </option>

        <option value="predictive">
          FlowMind Predictive
        </option>
      </select>

      <button
        className="primary-button full"
        onClick={onRun}
        disabled={running}
      >
        {running ? (
          <>
            Running simulation...
          </>
        ) : (
          <>
            <Play size={16} />
            Run scenario
          </>
        )}
      </button>

      <button
        className="secondary-button full"
      >
        <RotateCcw size={15} />
        Reset scenario
      </button>

    </div>
  );
}