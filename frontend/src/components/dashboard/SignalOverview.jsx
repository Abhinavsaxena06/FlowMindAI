import {
  ChevronRight,
} from "lucide-react";


const LANES = [
  "north",
  "east",
  "south",
  "west",
];


export default function SignalOverview({
  recommendation = null,
  traffic = null,
}) {

  const strategy =
    recommendation?.recommended_strategy ||
    {};


  const recommendedLane =
    strategy?.phase ||
    null;


  const duration =
    Number(
      strategy?.duration_seconds ||
      0
    );


  const currentPhase =
    recommendedLane ||
    traffic?.activeDirection ||
    "unknown";


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
          BACKEND ACTIVE
        </span>

      </div>


      <div className="signal-list">

        {LANES.map(
          (lane) => {

            const isGreen =
              lane ===
              recommendedLane;

            const state =
              isGreen
                ? "GREEN"
                : "RED";


            return (
              <div
                className="signal-row"
                key={lane}
              >

                <div className="signal-direction">

                  <span>
                    {lane.toUpperCase()}
                  </span>

                  <small>
                    Phase
                  </small>

                </div>


                <div className="signal-state">

                  <span
                    className={`signal-dot ${state.toLowerCase()}`}
                  />

                  <strong>
                    {state}
                  </strong>

                  <span>
                    {isGreen
                      ? `${duration}s`
                      : "—"}
                  </span>

                </div>

              </div>
            );
          }
        )}

      </div>


      <div className="panel-footer-link">

        Active recommendation:
        {" "}
        {currentPhase.toUpperCase()}

        <ChevronRight
          size={15}
        />

      </div>

    </div>
  );
}