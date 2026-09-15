import {
  ArrowDown,
  ArrowUp,
} from "lucide-react";

export default function MetricCard({
  title,
  value,
  unit,
  subtitle,
  icon: Icon,
  trend,
  tone = "default",
}) {
  const positive =
    Number(trend) >= 0;

  return (
    <div
      className={`metric-card ${tone}`}
    >

      <div className="metric-top">

        <div className="metric-icon">
          {Icon && <Icon size={18} />}
        </div>

        {trend !== undefined && (
          <div
            className={`metric-trend ${
              positive
                ? "up"
                : "down"
            }`}
          >
            {positive ? (
              <ArrowUp size={13} />
            ) : (
              <ArrowDown size={13} />
            )}

            {Math.abs(
              Number(trend)
            ).toFixed(1)}
            %
          </div>
        )}

      </div>

      <div className="metric-value">
        {value}
        {unit && (
          <span>{unit}</span>
        )}
      </div>

      <div className="metric-title">
        {title}
      </div>

      {subtitle && (
        <div className="metric-subtitle">
          {subtitle}
        </div>
      )}

    </div>
  );
}