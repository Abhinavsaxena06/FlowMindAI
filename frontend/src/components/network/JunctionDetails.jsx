import {
  Activity,
  ArrowDown,
  Car,
  Gauge,
} from "lucide-react";

export default function JunctionDetails({
  junction = "A",
}) {
  return (
    <div className="panel junction-details">

      <div className="panel-header">

        <div>
          <div className="eyebrow">
            JUNCTION DETAILS
          </div>

          <h2>
            Junction {junction}
          </h2>
        </div>

        <span className="badge warning">
          MODERATE
        </span>

      </div>

      <div className="detail-stat-grid">

        <div>
          <Car size={17} />
          <strong>147</strong>
          <span>Vehicles</span>
        </div>

        <div>
          <ArrowDown size={17} />
          <strong>38</strong>
          <span>Queue</span>
        </div>

        <div>
          <Gauge size={17} />
          <strong>31</strong>
          <span>km/h</span>
        </div>

        <div>
          <Activity size={17} />
          <strong>64%</strong>
          <span>Congestion</span>
        </div>

      </div>

      <div className="propagation-card">

        <span className="eyebrow">
          NETWORK PROPAGATION
        </span>

        <strong>
          Upstream pressure detected
        </strong>

        <p>
          Traffic pressure from connected
          approaches may influence this
          junction within the next cycle.
        </p>

      </div>

    </div>
  );
}