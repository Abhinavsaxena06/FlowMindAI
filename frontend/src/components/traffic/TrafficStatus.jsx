import {
  AlertTriangle,
  CheckCircle2,
} from "lucide-react";

import {
  statusTone,
} from "../../utils/traffic";

export default function TrafficStatus({
  status,
  score,
}) {
  const tone =
    statusTone(status);

  const normal =
    tone === "normal";

  const label =
    status || "UNKNOWN";

  const scoreValue =
    Number(score || 0);

  return (
    <div
      className={`traffic-status ${tone}`}
    >
      <div className="traffic-status-icon">
        {normal ? (
          <CheckCircle2 size={19} />
        ) : (
          <AlertTriangle size={19} />
        )}
      </div>

      <div className="traffic-status-content">
        <span>TRAFFIC STATUS</span>

        <strong>{label}</strong>

        <p>
          Congestion score{" "}
          <b>
            {scoreValue.toFixed(0)}
          </b>
          /100
        </p>
      </div>
    </div>
  );
}