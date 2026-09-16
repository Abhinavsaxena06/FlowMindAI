import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  ArrowDown,
  ArrowUp,
  Brain,
  Car,
  Clock3,
  Gauge,
  MapPin,
  ShieldCheck,
  TrendingUp,
  Zap,
} from "lucide-react";

const DEMO_LANES = [
  {
    id: "north",
    name: "North Lane",
    direction: "North",
    vehicles: 42,
    queue: 31,
    density: 68,
    speed: 24,
    trend: 12,
  },
  {
    id: "east",
    name: "East Lane",
    direction: "East",
    vehicles: 27,
    queue: 18,
    density: 46,
    speed: 35,
    trend: 5,
  },
  {
    id: "south",
    name: "South Lane",
    direction: "South",
    vehicles: 36,
    queue: 27,
    density: 59,
    speed: 28,
    trend: 9,
  },
  {
    id: "west",
    name: "West Lane",
    direction: "West",
    vehicles: 19,
    queue: 11,
    density: 32,
    speed: 42,
    trend: -4,
  },
];

function getStatus(density) {
  if (density >= 70) return "Critical";
  if (density >= 55) return "Heavy";
  if (density >= 40) return "Moderate";
  return "Normal";
}

function getStatusClass(status) {
  return status.toLowerCase();
}

export default function Prediction() {
  const [selectedLane, setSelectedLane] = useState("north");
  const [horizon, setHorizon] = useState(30);
  const [tick, setTick] = useState(0);

  // Fake live-looking movement — no API, no refresh button.
  useEffect(() => {
    const timer = setInterval(() => {
      setTick((value) => value + 1);
    }, 5000);

    return () => clearInterval(timer);
  }, []);

  const lanes = useMemo(() => {
    return DEMO_LANES.map((lane, index) => {
      const movement =
        Math.sin((tick + index) * 0.8) * 3 +
        Math.cos((tick + index) * 0.4) * 2;

      const density = Math.max(
        10,
        Math.min(92, Math.round(lane.density + movement))
      );

      const vehicles = Math.max(
        8,
        Math.round(lane.vehicles + movement)
      );

      const queue = Math.max(
        3,
        Math.round(lane.queue + movement * 0.8)
      );

      const speed = Math.max(
        12,
        Math.min(55, Math.round(lane.speed - movement * 0.7))
      );

      return {
        ...lane,
        density,
        vehicles,
        queue,
        speed,
        status: getStatus(density),
      };
    });
  }, [tick]);

  const selected = lanes.find((lane) => lane.id === selectedLane);

  const totalVehicles = lanes.reduce(
    (sum, lane) => sum + lane.vehicles,
    0
  );

  const totalQueue = lanes.reduce(
    (sum, lane) => sum + lane.queue,
    0
  );

  const averageDensity = Math.round(
    lanes.reduce((sum, lane) => sum + lane.density, 0) / lanes.length
  );

  const averageSpeed = Math.round(
    lanes.reduce((sum, lane) => sum + lane.speed, 0) / lanes.length
  );

  const overallStatus = getStatus(averageDensity);

  const predictedDensity = Math.min(
    95,
    Math.round(
      averageDensity +
        (horizon === 30 ? 7 : 13)
    )
  );

  const predictedQueue = Math.round(
    totalQueue * (horizon === 30 ? 1.12 : 1.23)
  );

  const predictedSpeed = Math.max(
    10,
    Math.round(
      averageSpeed -
        (horizon === 30 ? 4 : 8)
    )
  );

  const pressure = Math.min(
    100,
    Math.round(
      averageDensity * 0.72 +
        Math.min(totalQueue, 100) * 0.18 +
        10
    )
  );

  const chartPoints = [
    averageDensity - 8,
    averageDensity - 5,
    averageDensity - 2,
    averageDensity + 2,
    averageDensity + 5,
    predictedDensity,
  ].map((value) => Math.max(8, Math.min(95, value)));

  return (
    <div className="prediction-page">
      {/* HEADER */}
      <div className="prediction-header">
        <div>
          <div className="prediction-eyebrow">
            <Brain size={15} />
            AI TRAFFIC FORECAST
          </div>

          <h1>Traffic Prediction</h1>

          <p>
            Predict congestion before it builds up and understand what
            each traffic lane is doing.
          </p>
        </div>

        <div className="prediction-engine">
          <div className="engine-dot" />
          <div>
            <strong>Prediction Engine</strong>
            <span>Simulation active</span>
          </div>
        </div>
      </div>

      {/* MAIN STATUS */}
      <section className="prediction-hero">
        <div className="hero-status">
          <div className="hero-icon">
            <Activity size={27} />
          </div>

          <div>
            <span className="section-label">CURRENT TRAFFIC STATE</span>

            <div className="hero-status-row">
              <h2>{overallStatus}</h2>

              <span
                className={`prediction-status ${getStatusClass(
                  overallStatus
                )}`}
              >
                {averageDensity}% density
              </span>
            </div>

            <p>
              Traffic conditions are being simulated continuously
              across all monitored lanes.
            </p>
          </div>
        </div>

        <div className="prediction-location">
          <MapPin size={16} />
          <span>JUNCTION-A</span>
        </div>
      </section>

      {/* KPI GRID */}
      <div className="prediction-kpis">
        <div className="prediction-kpi">
          <div className="kpi-icon">
            <Car size={19} />
          </div>

          <div>
            <span>Total Vehicles</span>
            <strong>{totalVehicles}</strong>
          </div>

          <small>
            <ArrowUp size={13} />
            8.4%
          </small>
        </div>

        <div className="prediction-kpi">
          <div className="kpi-icon">
            <Clock3 size={19} />
          </div>

          <div>
            <span>Queue Length</span>
            <strong>{totalQueue}</strong>
          </div>

          <small>
            <ArrowUp size={13} />
            6.2%
          </small>
        </div>

        <div className="prediction-kpi">
          <div className="kpi-icon">
            <Gauge size={19} />
          </div>

          <div>
            <span>Avg. Speed</span>
            <strong>{averageSpeed} km/h</strong>
          </div>

          <small className="negative">
            <ArrowDown size={13} />
            4.8%
          </small>
        </div>

        <div className="prediction-kpi">
          <div className="kpi-icon">
            <TrendingUp size={19} />
          </div>

          <div>
            <span>Predicted Density</span>
            <strong>{predictedDensity}%</strong>
          </div>

          <small>
            +{predictedDensity - averageDensity}%
          </small>
        </div>
      </div>

      {/* FORECAST + PRESSURE */}
      <div className="prediction-main-grid">
        <section className="prediction-card forecast-card">
          <div className="prediction-card-header">
            <div>
              <span className="section-label">FORECAST</span>
              <h3>Congestion trajectory</h3>
            </div>

            <div className="horizon-tabs">
              <button
                className={horizon === 30 ? "active" : ""}
                onClick={() => setHorizon(30)}
              >
                30 sec
              </button>

              <button
                className={horizon === 60 ? "active" : ""}
                onClick={() => setHorizon(60)}
              >
                60 sec
              </button>
            </div>
          </div>

          <div className="forecast-chart">
            <div className="chart-grid">
              <span />
              <span />
              <span />
              <span />
            </div>

            <div className="chart-line">
              {chartPoints.map((point, index) => {
                const left = `${index * 19.5 + 2}%`;
                const top = `${100 - point}%`;

                return (
                  <div
                    key={index}
                    className={`chart-point ${
                      index === chartPoints.length - 1
                        ? "future"
                        : ""
                    }`}
                    style={{
                      left,
                      top,
                    }}
                  >
                    <span className="point-value">
                      {point}%
                    </span>
                  </div>
                );
              })}

              <div
                className="forecast-path"
                style={{
                  clipPath: `polygon(
                    2% ${100 - chartPoints[0]}%,
                    21.5% ${100 - chartPoints[1]}%,
                    41% ${100 - chartPoints[2]}%,
                    60.5% ${100 - chartPoints[3]}%,
                    80% ${100 - chartPoints[4]}%,
                    99% ${100 - chartPoints[5]}%,
                    99% 100%,
                    2% 100%
                  )`,
                }}
              />
            </div>

            <div className="chart-labels">
              <span>Now</span>
              <span>10s</span>
              <span>20s</span>
              <span>30s</span>
              <span>40s</span>
              <span>60s</span>
            </div>
          </div>

          <div className="forecast-message">
            <Zap size={17} />

            <div>
              <strong>
                {predictedDensity >= 70
                  ? "Congestion building ahead"
                  : "Traffic pressure increasing"}
              </strong>

              <span>
                Model expects density to reach approximately{" "}
                <b>{predictedDensity}%</b> within the selected
                horizon.
              </span>
            </div>
          </div>
        </section>

        {/* PRESSURE */}
        <section className="prediction-card pressure-card">
          <div className="prediction-card-header">
            <div>
              <span className="section-label">AI SIGNAL</span>
              <h3>Traffic pressure</h3>
            </div>

            <ShieldCheck size={20} />
          </div>

          <div className="pressure-gauge">
            <div
              className="pressure-ring"
              style={{
                "--pressure": `${pressure * 3.6}deg`,
              }}
            >
              <div>
                <strong>{pressure}</strong>
                <span>/ 100</span>
              </div>
            </div>
          </div>

          <div className="pressure-label">
            <span
              className={`prediction-status ${getStatusClass(
                getStatus(pressure)
              )}`}
            >
              {getStatus(pressure)}
            </span>

            <p>
              Composite score based on density, queues and vehicle
              load.
            </p>
          </div>

          <div className="pressure-bars">
            <div>
              <span>Density</span>
              <div>
                <i style={{ width: `${averageDensity}%` }} />
              </div>
              <b>{averageDensity}%</b>
            </div>

            <div>
              <span>Queue</span>
              <div>
                <i
                  style={{
                    width: `${Math.min(totalQueue, 100)}%`,
                  }}
                />
              </div>
              <b>{totalQueue}</b>
            </div>

            <div>
              <span>Vehicle load</span>
              <div>
                <i
                  style={{
                    width: `${Math.min(
                      (totalVehicles / 150) * 100,
                      100
                    )}%`,
                  }}
                />
              </div>
              <b>{totalVehicles}</b>
            </div>
          </div>
        </section>
      </div>

      {/* LANES */}
      <section className="prediction-card lanes-section">
        <div className="prediction-card-header">
          <div>
            <span className="section-label">LANE ANALYSIS</span>
            <h3>What each lane is doing</h3>
          </div>

          <span className="lane-count">
            {lanes.length} monitored lanes
          </span>
        </div>

        <div className="lane-grid">
          {lanes.map((lane) => (
            <button
              key={lane.id}
              className={`lane-card ${
                selectedLane === lane.id ? "selected" : ""
              }`}
              onClick={() => setSelectedLane(lane.id)}
            >
              <div className="lane-top">
                <div className="lane-direction">
                  <MapPin size={15} />
                  <strong>{lane.name}</strong>
                </div>

                <span
                  className={`prediction-status ${getStatusClass(
                    lane.status
                  )}`}
                >
                  {lane.status}
                </span>
              </div>

              <div className="lane-density">
                <strong>{lane.density}%</strong>
                <span>density</span>
              </div>

              <div className="lane-progress">
                <i
                  style={{
                    width: `${lane.density}%`,
                  }}
                />
              </div>

              <div className="lane-stats">
                <span>
                  <Car size={13} />
                  {lane.vehicles}
                </span>

                <span>
                  <Clock3 size={13} />
                  {lane.queue}
                </span>

                <span>{lane.speed} km/h</span>
              </div>
            </button>
          ))}
        </div>
      </section>

      {/* SELECTED LANE */}
      <section className="prediction-card selected-lane">
        <div className="selected-lane-title">
          <div className="selected-lane-icon">
            <Activity size={20} />
          </div>

          <div>
            <span className="section-label">SELECTED LANE</span>
            <h3>{selected.name}</h3>
          </div>
        </div>

        <div className="selected-lane-grid">
          <div>
            <span>Current density</span>
            <strong>{selected.density}%</strong>
          </div>

          <div>
            <span>Predicted density</span>
            <strong>
              {Math.min(
                95,
                selected.density +
                  (horizon === 30 ? 6 : 11)
              )}
              %
            </strong>
          </div>

          <div>
            <span>Queue</span>
            <strong>{selected.queue} vehicles</strong>
          </div>

          <div>
            <span>Average speed</span>
            <strong>{selected.speed} km/h</strong>
          </div>

          <div>
            <span>Traffic trend</span>
            <strong
              className={
                selected.trend >= 0
                  ? "trend-up"
                  : "trend-down"
              }
            >
              {selected.trend >= 0 ? "+" : ""}
              {selected.trend}%
            </strong>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <div className="prediction-footer-status">
        <div className="footer-pulse" />
        <span>
          AI simulation running • Traffic state updates
          automatically
        </span>
        <span className="footer-time">
          Horizon: {horizon} seconds
        </span>
      </div>
    </div>
  );
}