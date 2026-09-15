import {
  Activity,
  Database,
  Cpu,
  Radio,
} from "lucide-react";

const services = [
  {
    name: "Computer Vision",
    status: "Operational",
    icon: Cpu,
  },
  {
    name: "Traffic Engine",
    status: "Operational",
    icon: Activity,
  },
  {
    name: "State Store",
    status: "Operational",
    icon: Database,
  },
  {
    name: "Live Feed",
    status: "Connected",
    icon: Radio,
  },
];

export default function SystemStatus() {
  return (
    <div className="panel">

      <div className="panel-header">
        <div>
          <div className="eyebrow">
            PLATFORM
          </div>

          <h2>
            System health
          </h2>
        </div>

        <span className="status-dot live" />
      </div>

      <div className="service-list">

        {services.map(
          ({
            name,
            status,
            icon: Icon,
          }) => (
            <div
              className="service-row"
              key={name}
            >

              <div className="service-icon">
                <Icon size={16} />
              </div>

              <span>
                {name}
              </span>

              <div className="service-status">
                <span className="status-dot live" />
                {status}
              </div>

            </div>
          )
        )}

      </div>

    </div>
  );
}