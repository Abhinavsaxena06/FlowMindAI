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

  return (
    <div
      className={`traffic-status ${tone}`}
    >

      {normal ? (
        <CheckCircle2 size={18} />
      ) : (
        <AlertTriangle size={18} />
      )}

      <div>
        <strong>
          {status || "UNKNOWN"}
        </strong>

        <span>
          Congestion score{" "}
          {Number(score || 0).toFixed(0)}
        %
        </span>
      </div>

    </div>
  );
}