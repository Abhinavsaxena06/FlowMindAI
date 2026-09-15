import {
  ChevronRight,
} from "lucide-react";

const signals = [
  {
    lane: "NORTH",
    state: "GREEN",
    seconds: 34,
  },
  {
    lane: "EAST",
    state: "RED",
    seconds: 18,
  },
  {
    lane: "SOUTH",
    state: "RED",
    seconds: 12,
  },
  {
    lane: "WEST",
    state: "YELLOW",
    seconds: 4,
  },
];

export default function SignalOverview() {
  return (
    <div className="panel">

      <div className="panel-header">

        <div>
          <div className="eyebrow">
            SIGNAL CONTROL
          </div>

          <h2>
            Junction A
          </h2>
        </div>

        <span className="badge success">
          ADAPTIVE
        </span>

      </div>

      <div className="signal-list">

        {signals.map(
          (signal) => (
            <div
              className="signal-row"
              key={signal.lane}
            >

              <div className="signal-direction">
                <span>
                  {signal.lane}
                </span>

                <small>
                  Phase
                </small>
              </div>

              <div className="signal-state">

                <span
                  className={`signal-dot ${signal.state.toLowerCase()}`}
                />

                <strong>
                  {signal.state}
                </strong>

                <span>
                  {signal.seconds}s
                </span>

              </div>

            </div>
          )
        )}

      </div>

      <div className="panel-footer-link">
        View signal control
        <ChevronRight size={15} />
      </div>

    </div>
  );
}