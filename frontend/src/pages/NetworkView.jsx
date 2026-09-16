import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  Activity,
  AlertTriangle,
  Car,
  Gauge,
  Route,
  TimerReset,
  TrendingUp,
} from "lucide-react";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import useTrafficState from "../hooks/useTrafficState";
import {
  getTrafficHistory,
} from "../services/api";

const DIRECTION_KEYS = [
  "north",
  "south",
  "east",
  "west",
];

function safeNumber(
  value,
  fallback = 0
) {
  const parsed =
    Number(value ?? fallback);

  return Number.isFinite(parsed)
    ? parsed
    : fallback;
}

function getStatusLevel(
  score,
  label = ""
) {
  const value =
    Number(score || 0);
  const text =
    String(label || "")
      .toLowerCase();

  if (
    text.includes("severe") ||
    value >= 80
  ) {
    return "severe";
  }

  if (
    text.includes("high") ||
    value >= 60
  ) {
    return "high";
  }

  if (
    text.includes("moderate") ||
    value >= 35
  ) {
    return "moderate";
  }

  return "normal";
}

function formatTimeLabel(
  value
) {
  if (!value) {
    return "-";
  }

  if (
    typeof value === "number"
  ) {
    return `${value}s`;
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleTimeString(
    [],
    {
      hour: "2-digit",
      minute: "2-digit",
    }
  );
}

export default function NetworkView() {
  const {
    traffic,
    loading,
    connected,
    error,
  } = useTrafficState();

  const [history, setHistory] =
    useState([]);

  useEffect(() => {
    let mounted = true;

    async function loadHistory() {
      try {
        const data =
          await getTrafficHistory(
            60
          );

        if (!mounted) {
          return;
        }

        const items =
          Array.isArray(data)
            ? data
            : Array.isArray(
                data?.history
              )
            ? data.history
            : [];

        setHistory(items);
      } catch {
        if (mounted) {
          setHistory([]);
        }
      }
    }

    loadHistory();

    const timer = setInterval(
      loadHistory,
      5000
    );

    return () => {
      mounted = false;
      clearInterval(timer);
    };
  }, []);

  const graphData = useMemo(() => {
    const source =
      Array.isArray(history)
        ? history.slice(-60)
        : [];

    return source.map(
      (item, index) => {
        const approaches =
          item?.approaches ||
          item?.lane_counts ||
          {};

        return {
          label:
            formatTimeLabel(
              item?.timestamp ||
                item?.time ||
                index
            ),
          vehicles:
            safeNumber(
              item?.total_vehicles ??
                item?.current_vehicles ??
                item?.vehicle_count ??
                item?.overall?.total_vehicles ??
                0
            ),
          waiting:
            safeNumber(
              item?.waiting_vehicles ??
                item?.waiting ??
                item?.queue_count ??
                item?.queue_length ??
                item?.overall?.waiting_vehicles ??
                0
            ),
          queue:
            safeNumber(
              item?.queue_count ??
                item?.queue_length ??
                item?.overall_queue ??
                item?.overall?.queue_count ??
                0
            ),
          speed:
            safeNumber(
              item?.average_speed ??
                item?.avg_speed ??
                item?.overall?.average_speed ??
                0
            ),
          congestion:
            safeNumber(
              item?.congestion_score ??
                item?.congestion ??
                item?.overall?.congestion_score ??
                0
            ),
          north:
            safeNumber(
              approaches?.north?.vehicles ??
                approaches?.north?.vehicle_count ??
                approaches?.north ??
                0
            ),
          south:
            safeNumber(
              approaches?.south?.vehicles ??
                approaches?.south?.vehicle_count ??
                approaches?.south ??
                0
            ),
          east:
            safeNumber(
              approaches?.east?.vehicles ??
                approaches?.east?.vehicle_count ??
                approaches?.east ??
                0
            ),
          west:
            safeNumber(
              approaches?.west?.vehicles ??
                approaches?.west?.vehicle_count ??
                approaches?.west ??
                0
            ),
        };
      }
    );
  }, [history]);

  const summaryCards = useMemo(() => {
    const currentVehicles =
      safeNumber(
        traffic?.currentVehicles ??
          traffic?.totalVehicles ??
          0
      );
    const waitingVehicles =
      safeNumber(
        traffic?.waitingVehicles ??
          traffic?.queueCount ??
          0
      );
    const queueCount =
      safeNumber(
        traffic?.queueCount ?? 0
      );
    const passedVehicles =
      safeNumber(
        traffic?.passedVehicles ?? 0
      );
    const averageSpeed =
      safeNumber(
        traffic?.averageSpeed ?? 0
      );
    const congestionScore =
      safeNumber(
        traffic?.congestionScore ?? 0
      );

    return [
      {
        label: "Current Vehicles",
        value: currentVehicles,
        detail: "Active in network",
        icon: Car,
      },
      {
        label: "Waiting",
        value: waitingVehicles,
        detail: "Cars halted / queued",
        icon: TimerReset,
      },
      {
        label: "Queue",
        value: queueCount,
        detail: "Vehicles in queue",
        icon: Route,
      },
      {
        label: "Passed",
        value: passedVehicles,
        detail: "Completed pass-through",
        icon: TrendingUp,
      },
      {
        label: "Avg Speed",
        value: `${averageSpeed.toFixed(1)}`,
        detail: "Simulation speed",
        icon: Gauge,
      },
      {
        label: "Congestion",
        value: `${congestionScore.toFixed(0)}%`,
        detail:
          traffic?.congestionLevel ||
          traffic?.trafficStatus ||
          "Monitoring",
        icon: Activity,
      },
    ];
  }, [traffic]);

  const directionSummary = useMemo(
    () => {
      const raw =
        traffic?.raw || {};

      const approaches =
        raw.approaches ||
        raw.lane_counts ||
        {};

      return DIRECTION_KEYS.map(
        (key) => {
          const approach =
            approaches[key] || {};
          const vehicles = safeNumber(
            approach.vehicles ??
              approach.vehicle_count ??
              traffic?.laneCounts?.[key] ??
              0
          );

          const waiting = safeNumber(
            approach.waiting ??
              approach.queue ??
              0
          );

          const queue = safeNumber(
            approach.queue ??
              approach.waiting ??
              0
          );

          const speed = safeNumber(
            approach.avg_speed_kmh ??
              approach.speed_kmh ??
              traffic?.averageSpeed ??
              0
          );

          const congestion = safeNumber(
            approach.congestion ??
              approach.density ??
              0
          );

          return {
            key,
            name: key.toUpperCase(),
            vehicles,
            waiting,
            queue,
            speed,
            congestion,
          };
        }
      );
    },
    [traffic]
  );

  const currentStatus =
    getStatusLevel(
      traffic?.congestionScore,
      traffic?.congestionLevel ||
        traffic?.trafficStatus
    );

  const statusText =
    traffic?.congestionLevel ||
    traffic?.trafficStatus ||
    "Monitoring";

  const signalStatus =
    traffic?.signalState ||
    "UNKNOWN";

  const signalRemaining =
    traffic?.signalRemainingSeconds ??
    0;

  const hasData = Boolean(traffic);
  const noHistory = !graphData.length;

  return (
    <div className="page network-page">

      <section className="page-heading network-heading">

        <div>
          <div className="eyebrow">
            NETWORK TRAFFIC
          </div>

          <h1>
            Live network monitoring
          </h1>

          <p>
            Live traffic conditions, congestion,
            queues and vehicle movement across
            monitored directions.
          </p>
        </div>

        <div className="network-live-pill">
          <span
            className={`status-dot ${
              connected || hasData
                ? "live"
                : ""
            }`}
          />
          {connected || hasData
            ? "LIVE"
            : "IDLE"}
        </div>

      </section>

      <section className="network-summary-grid">
        {summaryCards.map(
          ({ label, value, detail, icon: Icon }) => (
            <div
              key={label}
              className="network-summary-card"
            >
              <div className="network-metric-icon">
                <Icon size={16} />
              </div>

              <div className="network-metric-value">
                {value}
              </div>

              <div className="network-metric-label">
                {label}
              </div>

              <div className="network-metric-detail">
                {detail}
              </div>
            </div>
          )
        )}
      </section>

      <div className="panel network-panel chart-panel-block">
        <div className="panel-header">
          <div>
            <div className="eyebrow">
              LIVE VEHICLE FLOW
            </div>

            <h2>
              Network throughput
            </h2>
          </div>

          <span className="chart-badge">
            Last 60s
          </span>
        </div>

        {noHistory ? (
          <div className="network-empty-state">
            {hasData
              ? "Collecting traffic data..."
              : "Start the simulation to view live network metrics."}
          </div>
        ) : (
          <div className="network-chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={graphData}>
                <CartesianGrid stroke="rgba(148, 163, 184, 0.12)" vertical={false} />
                <XAxis dataKey="label" tickLine={false} axisLine={false} tick={{ fill: "#94a3b8", fontSize: 10 }} />
                <YAxis tickLine={false} axisLine={false} tick={{ fill: "#94a3b8", fontSize: 10 }} />
                <Tooltip
                  contentStyle={{
                    background: "#0A1020",
                    border: "1px solid #24344D",
                    borderRadius: 12,
                    color: "#F8FAFC",
                  }}
                />
                <Line type="monotone" dataKey="vehicles" stroke="#00D9FF" strokeWidth={2.5} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      <div className="network-chart-grid">

        <div className="panel network-panel">
          <div className="panel-header">
            <div>
              <div className="eyebrow">
                QUEUE LENGTH
              </div>

              <h2>
                Live queue
              </h2>
            </div>
          </div>

          {noHistory ? (
            <div className="network-empty-state compact">
              {hasData
                ? "Collecting traffic data..."
                : "Start the simulation to view live network metrics."}
            </div>
          ) : (
            <div className="network-chart-container small">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={graphData}>
                  <CartesianGrid stroke="rgba(148, 163, 184, 0.12)" vertical={false} />
                  <XAxis dataKey="label" tickLine={false} axisLine={false} tick={{ fill: "#94a3b8", fontSize: 10 }} />
                  <YAxis tickLine={false} axisLine={false} tick={{ fill: "#94a3b8", fontSize: 10 }} />
                  <Tooltip
                    contentStyle={{
                      background: "#0A1020",
                      border: "1px solid #24344D",
                      borderRadius: 12,
                      color: "#F8FAFC",
                    }}
                  />
                  <Line type="monotone" dataKey="queue" stroke="#F59E0B" strokeWidth={2.5} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        <div className="panel network-panel">
          <div className="panel-header">
            <div>
              <div className="eyebrow">
                WAITING VEHICLES
              </div>

              <h2>
                Waiting traffic
              </h2>
            </div>
          </div>

          {noHistory ? (
            <div className="network-empty-state compact">
              {hasData
                ? "Collecting traffic data..."
                : "Start the simulation to view live network metrics."}
            </div>
          ) : (
            <div className="network-chart-container small">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={graphData}>
                  <CartesianGrid stroke="rgba(148, 163, 184, 0.12)" vertical={false} />
                  <XAxis dataKey="label" tickLine={false} axisLine={false} tick={{ fill: "#94a3b8", fontSize: 10 }} />
                  <YAxis tickLine={false} axisLine={false} tick={{ fill: "#94a3b8", fontSize: 10 }} />
                  <Tooltip
                    contentStyle={{
                      background: "#0A1020",
                      border: "1px solid #24344D",
                      borderRadius: 12,
                      color: "#F8FAFC",
                    }}
                  />
                  <Line type="monotone" dataKey="waiting" stroke="#22C55E" strokeWidth={2.5} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

      </div>

      <div className="panel network-panel">
        <div className="panel-header">
          <div>
            <div className="eyebrow">
              DIRECTION-WISE FLOW
            </div>

            <h2>
              North • South • East • West
            </h2>
          </div>
        </div>

        {noHistory ? (
          <div className="network-empty-state compact">
            {hasData
              ? "Collecting traffic data..."
              : "Start the simulation to view live network metrics."}
          </div>
        ) : (
          <>
            <div className="network-direction-grid">
              {directionSummary.map(
                ({ name, vehicles, waiting, queue, speed, congestion }) => (
                  <div
                    key={name}
                    className="network-direction-card"
                  >
                    <div className="network-direction-name">
                      {name}
                    </div>

                    <div className="network-direction-row">
                      <span>Vehicles</span>
                      <strong>{vehicles}</strong>
                    </div>

                    <div className="network-direction-row">
                      <span>Waiting</span>
                      <strong>{waiting}</strong>
                    </div>

                    <div className="network-direction-row">
                      <span>Queue</span>
                      <strong>{queue}</strong>
                    </div>

                    <div className="network-direction-row">
                      <span>Speed</span>
                      <strong>
                        {speed > 0 ? `${speed.toFixed(1)}` : "—"}
                      </strong>
                    </div>

                    <div className="network-direction-row">
                      <span>Congestion</span>
                      <strong>
                        {congestion > 0 ? `${congestion.toFixed(0)}%` : "—"}
                      </strong>
                    </div>
                  </div>
                )
              )}
            </div>

            <div className="network-chart-container small top-margin">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={graphData.slice(-12)}>
                  <CartesianGrid stroke="rgba(148, 163, 184, 0.12)" vertical={false} />
                  <XAxis dataKey="label" tickLine={false} axisLine={false} tick={{ fill: "#94a3b8", fontSize: 10 }} />
                  <YAxis tickLine={false} axisLine={false} tick={{ fill: "#94a3b8", fontSize: 10 }} />
                  <Tooltip
                    contentStyle={{
                      background: "#0A1020",
                      border: "1px solid #24344D",
                      borderRadius: 12,
                      color: "#F8FAFC",
                    }}
                  />
                  <Bar dataKey="north" fill="#00D9FF" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="south" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="east" fill="#60A5FA" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="west" fill="#93C5FD" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </>
        )}
      </div>

      <div className="network-status-grid">

        <div className="panel network-panel status-panel">
          <div className="panel-header">
            <div>
              <div className="eyebrow">
                NETWORK STATUS
              </div>

              <h2>
                Live conditions
              </h2>
            </div>
          </div>

          <div className={`network-status-badge ${currentStatus}`}>
            {statusText || "Monitoring"}
          </div>

          <div className="network-status-meta">
            <div>
              <span>Congestion</span>
              <strong>
                {safeNumber(traffic?.congestionScore ?? 0).toFixed(0)}%
              </strong>
            </div>

            <div>
              <span>Queue</span>
              <strong>
                {safeNumber(traffic?.queueCount ?? 0)}
              </strong>
            </div>

            <div>
              <span>Speed</span>
              <strong>
                {safeNumber(traffic?.averageSpeed ?? 0).toFixed(1)}
              </strong>
            </div>
          </div>
        </div>

        <div className="panel network-panel status-panel">
          <div className="panel-header">
            <div>
              <div className="eyebrow">
                SIGNAL / PHASE STATUS
              </div>

              <h2>
                Active signal state
              </h2>
            </div>
          </div>

          <div className="signal-badge-row">
            <span className="signal-phase-badge">
              {signalStatus}
            </span>

            {signalRemaining > 0 && (
              <span className="signal-remaining">
                {signalRemaining}s remaining
              </span>
            )}
          </div>

          <div className="network-status-meta">
            <div>
              <span>Phase</span>
              <strong>{signalStatus}</strong>
            </div>

            <div>
              <span>Direction</span>
              <strong>
                {traffic?.activeDirection || "—"}
              </strong>
            </div>

            <div>
              <span>Condition</span>
              <strong>{statusText || "Monitoring"}</strong>
            </div>
          </div>
        </div>

      </div>

      {error && (
        <div className="network-error">
          <AlertTriangle size={14} />
          {error}
        </div>
      )}

    </div>
  );
}