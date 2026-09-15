import {
  Activity,
  BrainCircuit,
  ChevronRight,
  CircleGauge,
  GitBranch,
  LayoutDashboard,
  Radio,
  TrafficCone,
} from "lucide-react";

import {
  NavLink,
} from "react-router-dom";

const navigation = [
  {
    section: "COMMAND CENTER",
    items: [
      {
        label: "Overview",
        path: "/",
        icon: LayoutDashboard,
      },
      {
        label: "Live Monitoring",
        path: "/live",
        icon: Radio,
      },
      {
        label: "AI Predictions",
        path: "/predictions",
        icon: BrainCircuit,
      },
    ],
  },
  {
    section: "TRAFFIC CONTROL",
    items: [
      {
        label: "Signal Control",
        path: "/signals",
        icon: TrafficCone,
      },
      {
        label: "Network",
        path: "/network",
        icon: GitBranch,
      },
      {
        label: "Simulation",
        path: "/simulation",
        icon: CircleGauge,
      },
    ],
  },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">

      {/* BRAND */}

      <div className="brand">

        <div className="brand-icon">
          <Activity size={18} />
        </div>

        <div className="brand-text">
          <strong>FlowMind</strong>
          <span>Traffic Intelligence</span>
        </div>

      </div>


      {/* NAVIGATION */}

      <div className="sidebar-scroll">

        {navigation.map((group) => (
          <div
            className="sidebar-section"
            key={group.section}
          >

            <div className="sidebar-section-title">
              {group.section}
            </div>

            <nav className="nav">

              {group.items.map((item) => {
                const Icon = item.icon;

                return (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    end={item.path === "/"}
                    className={({ isActive }) =>
                      `nav-item ${
                        isActive
                          ? "active"
                          : ""
                      }`
                    }
                  >

                    <Icon className="nav-icon" />

                    <span>
                      {item.label}
                    </span>

                    <ChevronRight
                      className="nav-arrow"
                      size={14}
                    />

                  </NavLink>
                );
              })}

            </nav>

          </div>
        ))}

      </div>


      {/* FOOTER */}

      <div className="sidebar-footer">

        <div className="system-online">

          <span className="system-online-dot" />

          <span>System Online</span>

        </div>

        <div className="sidebar-version">
          FlowMind v1.0 • Demo
        </div>

      </div>

    </aside>
  );
}