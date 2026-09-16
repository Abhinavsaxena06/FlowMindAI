import {
  useEffect,
  useState,
} from "react";

import JunctionSignal from "../components/signals/JunctionSignal";
import SignalRecommendation from "../components/signals/SignalRecommendation";
import EmergencyCorridor from "../components/signals/EmergencyCorridor";

import {
  getTrafficState,
  getTrafficRecommendation,
} from "../services/api";


const LANES = [
  "north",
  "east",
  "south",
  "west",
];


export default function SignalControl() {

  const [
    traffic,
    setTraffic,
  ] = useState(null);


  const [
    recommendation,
    setRecommendation,
  ] = useState(null);


  useEffect(() => {

    let mounted = true;


    async function loadData() {

      try {

        const [
          state,
          signalRecommendation,
        ] = await Promise.all([
          getTrafficState(),
          getTrafficRecommendation(),
        ]);


        if (!mounted) {
          return;
        }


        setTraffic(
          state?.status === "waiting"
            ? null
            : state
        );


        setRecommendation(
          signalRecommendation
        );

      } catch {
        // Keep existing UI alive.
      }
    }


    loadData();

    const timer =
      setInterval(
        loadData,
        1000
      );


    return () => {
      mounted = false;
      clearInterval(timer);
    };

  }, []);


  const strategy =
    recommendation?.recommended_strategy ||
    {};


  const activeLane =
    strategy.phase ||
    null;


  const duration =
    Number(
      strategy.duration_seconds ||
      0
    );


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
            {traffic?.timestamp
              ? "LIVE"
              : "WAITING FOR DATA"}
          </span>

        </div>


        <div className="junction-grid">

          {LANES.map(
            (lane) => {

              const isActive =
                lane ===
                activeLane;


              return (
                <JunctionSignal
                  key={lane}
                  direction={
                    lane.toUpperCase()
                  }
                  state={
                    isActive
                      ? "GREEN"
                      : "RED"
                  }
                  seconds={
                    isActive
                      ? duration
                      : 0
                  }
                />
              );
            }
          )}

        </div>

      </div>


      <div className="dashboard-grid signal-grid">

        <SignalRecommendation
          recommendation={
            recommendation
          }
          traffic={traffic}
        />

        <EmergencyCorridor />

      </div>

    </div>
  );
}