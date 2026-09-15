import CameraView from "../components/traffic/CameraView";
import LaneCard from "../components/traffic/LaneCard";
import VehicleBreakdown from "../components/traffic/VehicleBreakdown";
import TrafficStatus from "../components/traffic/TrafficStatus";

import useTrafficState from "../hooks/useTrafficState";

export default function LiveMonitoring() {
  const {
    traffic,
    loading,
    connected,
  } = useTrafficState();

  if (
    loading &&
    !traffic
  ) {
    return (
      <div className="page-loading">
        <div className="loader" />
        Connecting to traffic engine...
      </div>
    );
  }

  const lanes =
    traffic?.laneCounts || {};

  return (
    <div className="page">

      <section className="page-heading">

        <div>
          <div className="eyebrow">
            LIVE MONITORING
          </div>

          <h1>
            Traffic perception
          </h1>

          <p>
            Computer vision and tracking
            from the active traffic feed.
          </p>
        </div>

        <div className="connection-pill">
          <span
            className={`status-dot ${
              connected
                ? "live"
                : ""
            }`}
          />
          {connected
            ? "Streaming"
            : "Polling"}
        </div>

      </section>

      <div className="live-grid">

        <CameraView />

        <TrafficStatus
          status={
            traffic?.trafficStatus
          }
          score={
            traffic?.congestionScore
          }
        />

      </div>

      <section className="section-heading">
        <div>
          <span className="eyebrow">
            LANE INTELLIGENCE
          </span>

          <h2>
            Approach conditions
          </h2>
        </div>
      </section>

      <div className="lane-grid">

        <LaneCard
          direction="NORTH"
          count={lanes.north}
          speed={
            traffic?.averageSpeed
          }
        />

        <LaneCard
          direction="EAST"
          count={lanes.east}
          speed={
            traffic?.averageSpeed
          }
        />

        <LaneCard
          direction="SOUTH"
          count={lanes.south}
          speed={
            traffic?.averageSpeed
          }
        />

        <LaneCard
          direction="WEST"
          count={lanes.west}
          speed={
            traffic?.averageSpeed
          }
        />

      </div>

      <VehicleBreakdown />

    </div>
  );
}