import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  Car,
  Gauge,
  RefreshCw,
  TriangleAlert,
  Clock3,
} from "lucide-react";

const API_URL = "http://127.0.0.1:8000/api/traffic/current";

export default function LiveMonitoring() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchTraffic = async (manual = false) => {
    try {
      if (manual) {
        setRefreshing(true);
      }

      setError("");

      const response = await fetch(API_URL);

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }

      const result = await response.json();

      setData(result);
      setLastUpdated(new Date());
    } catch (err) {
      console.error("Live monitoring error:", err);
      setError(
        "Unable to connect to the traffic server. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchTraffic();

    const interval = setInterval(() => {
      fetchTraffic();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const summary = useMemo(() => {
    const lanes = Object.values(data?.lanes || {});

    if (lanes.length === 0) {
      return {
        vehicles: 0,
        queue: 0,
        speed: 0,
        density: 0,
        status: "Normal",
      };
    }

    const vehicles = lanes.reduce(
      (total, lane) => total + Number(lane.vehicle_count || 0),
      0
    );

    const queue = lanes.reduce(
      (total, lane) => total + Number(lane.queue_length || 0),
      0
    );

    const speed =
      lanes.reduce(
        (total, lane) => total + Number(lane.avg_speed || 0),
        0
      ) / lanes.length;

    const density =
      lanes.reduce(
        (total, lane) => total + Number(lane.density || 0),
        0
      ) / lanes.length;

    let status = "Normal";

    if (density >= 0.8 || queue >= 70) {
      status = "Critical";
    } else if (density >= 0.6 || queue >= 40) {
      status = "Heavy";
    } else if (density >= 0.4) {
      status = "Moderate";
    }

    return {
      vehicles,
      queue,
      speed,
      density,
      status,
    };
  }, [data]);

  const lanes = Object.entries(data?.lanes || {});

  if (loading) {
    return (
      <div className="fm-page">
        <div className="fm-loading">
          <RefreshCw className="fm-spin" size={24} />
          <span>Loading live traffic data...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="fm-page">
      {/* HEADER */}
      <div className="fm-page-header">
        <div>
          <div className="fm-eyebrow">
            <span className="fm-live-dot" />
            LIVE SYSTEM
          </div>

          <h1>Live Monitoring</h1>

          <p>
            Real-time traffic conditions across monitored junctions.
          </p>
        </div>

        <button
          className="fm-button"
          onClick={() => fetchTraffic(true)}
          disabled={refreshing}
        >
          <RefreshCw
            size={16}
            className={refreshing ? "fm-spin" : ""}
          />
          {refreshing ? "Refreshing..." : "Refresh"}
        </button>
      </div>

      {/* ERROR */}
      {error && (
        <div className="fm-error">
          <TriangleAlert size={20} />

          <div>
            <strong>Connection problem</strong>
            <p>{error}</p>
          </div>

          <button
            className="fm-error-button"
            onClick={() => fetchTraffic(true)}
          >
            Retry
          </button>
        </div>
      )}

      {/* JUNCTION STATUS */}
      <div className="fm-status-bar">
        <div className="fm-status-left">
          <Activity size={18} />

          <div>
            <span className="fm-small-label">MONITORED JUNCTION</span>
            <strong>{data?.junction || "JUNCTION-A"}</strong>
          </div>
        </div>

        <div className={`fm-status ${getStatusClass(summary.status)}`}>
          <span />
          {summary.status}
        </div>

        <div className="fm-updated">
          <Clock3 size={15} />

          {lastUpdated
            ? `Updated ${lastUpdated.toLocaleTimeString()}`
            : "Waiting for update"}
        </div>
      </div>

      {/* METRICS */}
      <div className="fm-metrics">
        <MetricCard
          icon={<Car size={21} />}
          label="Total Vehicles"
          value={summary.vehicles}
          description="Currently detected"
        />

        <MetricCard
          icon={<TriangleAlert size={21} />}
          label="Queue Length"
          value={summary.queue}
          suffix=" vehicles"
          description="Current estimated queue"
        />

        <MetricCard
          icon={<Gauge size={21} />}
          label="Average Speed"
          value={summary.speed.toFixed(1)}
          suffix=" km/h"
          description="Across monitored lanes"
        />

        <MetricCard
          icon={<Activity size={21} />}
          label="Traffic Density"
          value={(summary.density * 100).toFixed(0)}
          suffix="%"
          description="Current road occupancy"
        />
      </div>

      {/* LANE TABLE */}
      <section className="fm-card">
        <div className="fm-card-header">
          <div>
            <h2>Lane Conditions</h2>
            <p>Live traffic state for each direction.</p>
          </div>

          <span className="fm-data-badge">
            {lanes.length} lanes
          </span>
        </div>

        {lanes.length === 0 ? (
          <div className="fm-empty">
            No lane data is currently available.
          </div>
        ) : (
          <div className="fm-table-wrapper">
            <div className="fm-table fm-table-head">
              <span>Lane</span>
              <span>Vehicles</span>
              <span>Queue</span>
              <span>Density</span>
              <span>Avg. Speed</span>
            </div>

            {lanes.map(([laneName, lane]) => (
              <div className="fm-table" key={laneName}>
                <strong>
                  {laneName.toUpperCase()}
                </strong>

                <span>
                  {lane.vehicle_count ?? 0}
                </span>

                <span>
                  {lane.queue_length ?? 0}
                </span>

                <span>
                  {(
                    Number(lane.density || 0) * 100
                  ).toFixed(0)}
                  %
                </span>

                <span>
                  {Number(lane.avg_speed || 0).toFixed(1)} km/h
                </span>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

function MetricCard({
  icon,
  label,
  value,
  suffix = "",
  description,
}) {
  return (
    <div className="fm-metric-card">
      <div className="fm-metric-icon">
        {icon}
      </div>

      <div className="fm-metric-content">
        <span>{label}</span>

        <strong>
          {value}
          <small>{suffix}</small>
        </strong>

        <p>{description}</p>
      </div>
    </div>
  );
}

function getStatusClass(status) {
  if (status === "Critical") return "critical";
  if (status === "Heavy") return "heavy";
  if (status === "Moderate") return "moderate";

  return "normal";
}