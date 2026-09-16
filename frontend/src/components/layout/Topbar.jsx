import {
  Bell,
  ChevronDown,
  MapPin,
  Menu,
  Radio,
} from "lucide-react";

import {
  useLocation,
} from "react-router-dom";

const pageNames = {
  "/": "Overview",
  "/live": "Live Monitoring",
  "/predictions": "AI Predictions",
  "/pedestrian-safety": "Pedestrian Safety",
  "/signals": "Signal Control",
  "/network": "Network",
  "/simulation": "Simulation",
};

export default function Topbar() {
  const location = useLocation();

  const currentPage =
    pageNames[location.pathname] ||
    "FlowMind";

  return (
    <header className="topbar">

      <div className="topbar-left">

        <button
          className="mobile-menu-button"
          type="button"
          aria-label="Open navigation"
        >
          <Menu size={18} />
        </button>

        <div className="topbar-location">

          <MapPin size={15} />

          <span>
            Bhopal Traffic Network
          </span>

        </div>

        <div className="topbar-divider" />

        <span className="topbar-page">
          {currentPage}
        </span>

      </div>


      <div className="topbar-right">

        <div className="network-status">

          <span className="network-status-dot" />

          <Radio size={13} />

          <span>
            Network Online
          </span>

        </div>


        <button
          className="icon-button"
          type="button"
          aria-label="Notifications"
        >
          <Bell size={17} />

          <span className="notification-dot" />

        </button>


        <div className="operator">

          <div className="operator-avatar">
            OP
          </div>

          <div className="operator-info">
            <strong>Operator</strong>
            <span>Control Room</span>
          </div>

          <ChevronDown size={14} />

        </div>

      </div>

    </header>
  );
}