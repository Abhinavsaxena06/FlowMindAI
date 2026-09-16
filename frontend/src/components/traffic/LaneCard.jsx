import {
  ArrowUpRight,
  Car,
  Gauge,
} from "lucide-react";

export default function LaneCard({
  direction,
  count,
  speed = 0,
}) {
  const intensity =
    Math.min(
      100,
      Number(count || 0) * 3
    );

  return (
    <div className="lane-card">

      <div className="lane-card-top">

        <div className="lane-card-heading">
          <span className="eyebrow">
            APPROACH
          </span>

          <h3>
            {direction}
          </h3>
        </div>

        <ArrowUpRight size={17} />

      </div>

      <div className="lane-number-row">
        <div className="lane-number">
          {count}
        </div>
      </div>

      <div className="lane-meta">

        <span>
          <Car size={14} />
          Vehicles
        </span>

        <span>
          <Gauge size={14} />
          <strong>{Number(speed).toFixed(1)}</strong>
          <em>km/h</em>
        </span>

      </div>

      <div className="lane-bar">
        <span
          style={{
            width: `${intensity}%`,
          }}
        />
      </div>

    </div>
  );
}