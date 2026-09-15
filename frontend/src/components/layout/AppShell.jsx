import { NavLink, Outlet } from "react-router-dom";

import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import MobileNav from "./MobileNav";

const platformLinks = [
  { label: "Dashboard", to: "/" },
  { label: "Simulation", to: "/simulation" },
  { label: "Network", to: "/network" },
  { label: "Traffic Updates", to: "/live" },
  { label: "Predictions", to: "/predictions" },
  { label: "Signal Controls", to: "/signals" },
];

const emergencyLinks = [
  { label: "Emergency Corridor", to: "/signals" },
];

export default function AppShell() {
  return (
    <div className="app-shell">

      <Sidebar />

      <div className="main-shell">

        <Topbar />

        <main className="page-content">
          <div className="page-shell">
            <Outlet />
          </div>
        </main>

        <footer className="site-footer">
          <div className="site-footer-inner page-shell">
            <div className="site-footer-rule" />

            <div className="site-footer-grid">
              <div className="site-footer-brand">
                <div className="site-footer-title">FLOWMIND AI</div>
                <p>Predictive Traffic Intelligence</p>
              </div>

              <div className="site-footer-column">
                <h3>Platform</h3>
                <nav className="site-footer-nav" aria-label="Platform navigation">
                  {platformLinks.map((item) => (
                    <NavLink
                      key={item.to + item.label}
                      to={item.to}
                      end={item.to === "/"}
                    >
                      {item.label}
                    </NavLink>
                  ))}
                </nav>
              </div>

              <div className="site-footer-column">
                <h3>Emergency</h3>
                <nav className="site-footer-nav" aria-label="Emergency navigation">
                  {emergencyLinks.map((item) => (
                    <NavLink
                      key={item.to + item.label}
                      to={item.to}
                    >
                      {item.label}
                    </NavLink>
                  ))}
                </nav>
              </div>
            </div>

            <div className="site-footer-rule site-footer-rule-bottom" />

            <div className="site-footer-meta">
              <span>© FlowMind AI</span>
            </div>
          </div>
        </footer>

      </div>

      <MobileNav />

    </div>
  );
}