import {
  BrainCircuit,
  CircleGauge,
  Footprints,
  LayoutDashboard,
  Radio,
  TrafficCone,
} from "lucide-react";

import {
  NavLink,
} from "react-router-dom";

const items = [
  {
    label: "Home",
    path: "/",
    icon: LayoutDashboard,
  },
  {
    label: "Live",
    path: "/live",
    icon: Radio,
  },
  {
    label: "AI",
    path: "/predictions",
    icon: BrainCircuit,
  },
  {
    label: "Ped",
    path: "/pedestrian-safety",
    icon: Footprints,
  },
  {
    label: "Signals",
    path: "/signals",
    icon: TrafficCone,
  },
  {
    label: "Sim",
    path: "/simulation",
    icon: CircleGauge,
  },
];

export default function MobileNav() {
  return (
    <nav className="mobile-nav">

      {items.map((item) => {
        const Icon = item.icon;

        return (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === "/"}
            className={({ isActive }) =>
              `mobile-nav-item ${
                isActive
                  ? "active"
                  : ""
              }`
            }
          >

            <Icon size={18} />

            <span>
              {item.label}
            </span>

          </NavLink>
        );
      })}

    </nav>
  );
}