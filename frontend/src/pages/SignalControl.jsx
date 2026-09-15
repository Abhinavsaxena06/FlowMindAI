import JunctionSignal from "../components/signals/JunctionSignal";
import SignalRecommendation from "../components/signals/SignalRecommendation";
import EmergencyCorridor from "../components/signals/EmergencyCorridor";

export default function SignalControl() {
  return (
    <div className="page signal-page">

      <section className="page-heading">

        <div>
          <div className="eyebrow">
            SIGNAL INTELLIGENCE
          </div>

          <h1>
            Junction control
          </h1>

          <p>
            Decision support for adaptive,
            predictive and emergency signal
            strategies.
          </p>
        </div>

        <span className="badge success">
          PREDICTIVE MODE
        </span>

      </section>

      <div className="junction-board">

        <div className="junction-board-header">
          <div>
            <span className="eyebrow">
              ACTIVE JUNCTION
            </span>

            <h2>
              Junction A
            </h2>
          </div>

          <span>
            Cycle 42 / 90s
          </span>
        </div>

        <div className="junction-grid">

          <JunctionSignal
            direction="NORTH"
            state="GREEN"
            seconds={34}
          />

          <JunctionSignal
            direction="EAST"
            state="RED"
            seconds={18}
          />

          <JunctionSignal
            direction="SOUTH"
            state="RED"
            seconds={12}
          />

          <JunctionSignal
            direction="WEST"
            state="YELLOW"
            seconds={4}
          />

        </div>

      </div>

      <div className="dashboard-grid signal-grid">

        <SignalRecommendation />

        <EmergencyCorridor />

      </div>

    </div>
  );
}