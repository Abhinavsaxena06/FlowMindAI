import {
  Activity,
  Car,
  Gauge,
  Timer,
} from "lucide-react";

import MetricCard from "../components/dashboard/MetricCard";
import TrafficOverview from "../components/dashboard/TrafficOverview";
import SignalOverview from "../components/dashboard/SignalOverview";
import PredictionOverview from "../components/dashboard/PredictionOverview";
import SystemStatus from "../components/dashboard/SystemStatus";

import useTrafficState from "../hooks/useTrafficState";
import usePrediction from "../hooks/usePrediction";

import {
  getTrafficHistory,
  getTrafficRecommendation,
} from "../services/api";

import {
  useEffect,
  useState,
} from "react";


export default function Dashboard() {

  const {
    traffic,
    loading,
    connected,
  } = useTrafficState();


  const {
    prediction,
  } = usePrediction();


  const [
    history,
    setHistory,
  ] = useState([]);


  const [
    recommendation,
    setRecommendation,
  ] = useState(null);


  // ============================================================
  // REAL BACKEND HISTORY
  // ============================================================

  useEffect(() => {

    let mounted = true;


    async function loadHistory() {

      try {

        const data =
          await getTrafficHistory(30);


        if (!mounted) {
          return;
        }


        if (Array.isArray(data)) {

          setHistory(data);

          return;
        }


        if (
          Array.isArray(
            data?.history
          )
        ) {

          setHistory(
            data.history
          );
        }

      } catch {
        // Keep live traffic working
        // if history is temporarily unavailable.
      }
    }


    loadHistory();


    const timer =
      setInterval(
        loadHistory,
        2000
      );


    return () => {

      mounted = false;

      clearInterval(timer);

    };

  }, []);


  // ============================================================
  // REAL BACKEND SIGNAL RECOMMENDATION
  // ============================================================

  useEffect(() => {

    let mounted = true;


    async function loadRecommendation() {

      try {

        const data =
          await getTrafficRecommendation();


        if (!mounted) {
          return;
        }


        if (
          data?.status ===
          "warming_up"
        ) {

          setRecommendation(null);

          return;
        }


        setRecommendation(data);

      } catch {
        // Do not break dashboard
        // if recommendation is temporarily unavailable.
      }
    }


    loadRecommendation();


    const timer =
      setInterval(
        loadRecommendation,
        1500
      );


    return () => {

      mounted = false;

      clearInterval(timer);

    };

  }, []);


  // ============================================================
  // LOADING
  // ============================================================

  if (
    loading &&
    !traffic
  ) {

    return (
      <div className="page-loading">

        <div className="loader" />

        <span>
          Loading command center...
        </span>

      </div>
    );
  }


  // ============================================================
  // LIVE TRAFFIC VALUES
  // ============================================================

  const totalVehicles =
    traffic?.currentVehicles ??
    traffic?.totalVehicles ??
    0;


  const passedVehicles =
    traffic?.passedVehicles ??
    0;


  const waitingVehicles =
    traffic?.waitingVehicles ??
    traffic?.queueCount ??
    0;


  const queueCount =
    traffic?.queueCount ??
    0;


  const averageSpeed =
    Number(
      traffic?.averageSpeed ??
      0
    );


  const density =
    Number(
      traffic?.density ??
      0
    );


  const congestion =
    Number(
      traffic?.congestionScore ??
      0
    );


  const congestionLevel =
    traffic?.congestionLevel ||
    traffic?.trafficStatus ||
    "UNKNOWN";


  const signalState =
    traffic?.signalState ||
    "UNKNOWN";


  const signalRemaining =
    Number(
      traffic?.signalRemainingSeconds ??
      0
    );


  return (
    <div className="page dashboard-page">

      {/* =================================================
          HERO
          ================================================= */}

      <section className="hero">

        <div className="hero-copy">

          <div className="eyebrow">
            TRAFFIC COMMAND CENTER
          </div>

          <h1>
            Predict traffic.
            <br />
            <span>
              Move the city smarter.
            </span>
          </h1>

          <p>
            Real-time traffic intelligence,
            predictive analytics and adaptive
            signal decision support.
          </p>

        </div>


        <div className="hero-status">

          <span
            className={`status-dot ${
              connected
                ? "live"
                : ""
            }`}
          />

          <div>

            <strong>
              {connected
                ? "LIVE DATA"
                : "POLLING MODE"}
            </strong>

            <span>
              {connected
                ? "Traffic network connected"
                : "Using periodic updates"}
            </span>

          </div>

        </div>

      </section>


      {/* =================================================
          KPI METRICS
          ================================================= */}

      <section className="metrics-grid">

        <MetricCard
          title="Current vehicles"
          value={totalVehicles}
          subtitle="Active in traffic network"
          icon={Car}
        />


        <MetricCard
          title="Vehicles passed"
          value={passedVehicles}
          subtitle="Completed passes"
          icon={Activity}
        />


        <MetricCard
          title="Waiting vehicles"
          value={waitingVehicles}
          subtitle="Stopped / queued"
          icon={Timer}
          tone={
            waitingVehicles > 10
              ? "warning"
              : "default"
          }
        />


        <MetricCard
          title="Queue length"
          value={queueCount}
          subtitle="Vehicles waiting"
          icon={Timer}
          tone={
            queueCount > 30
              ? "warning"
              : "default"
          }
        />


        <MetricCard
          title="Average speed"
          value={averageSpeed.toFixed(1)}
          unit="km/h"
          subtitle="Live traffic speed"
          icon={Gauge}
        />


        <MetricCard
          title="Traffic density"
          value={
            density <= 1
              ? density.toFixed(2)
              : (density / 100).toFixed(2)
          }
          subtitle="Live junction density"
          icon={Gauge}
        />


        <MetricCard
          title="Congestion"
          value={congestion.toFixed(0)}
          unit="%"
          subtitle={
            congestionLevel ||
            "Monitoring"
          }
          icon={Activity}
          tone={
            congestion >= 70
              ? "danger"
              : congestion >= 40
                ? "warning"
                : "default"
          }
        />


        <MetricCard
          title="Current signal"
          value={
            signalState
          }
          subtitle={
            signalRemaining
              ? `${signalRemaining}s remaining`
              : recommendation?.recommended_strategy?.phase
                ? `AI: ${String(
                    recommendation
                      .recommended_strategy
                      .phase
                  ).toUpperCase()}`
                : "Signal status"
          }
          icon={Activity}
        />

      </section>


      {/* =================================================
          TRAFFIC + SIGNALS
          ================================================= */}

      <section className="dashboard-grid dashboard-grid-primary">

        <div className="dashboard-main-card">

          <TrafficOverview
            history={history}
          />

        </div>


        <div className="dashboard-side-card">

          <SignalOverview
            recommendation={
              recommendation
            }
            traffic={
              traffic
            }
          />

        </div>

      </section>


      {/* =================================================
          PREDICTION + SYSTEM
          ================================================= */}

      <section className="dashboard-grid dashboard-grid-secondary">

        <div className="dashboard-main-card">

          <PredictionOverview
            prediction={
              prediction
            }
          />

        </div>


        <div className="dashboard-side-card">

          <SystemStatus />

        </div>

      </section>

    </div>
  );
}