import {
  useMemo,
} from "react";

import {
  Area,
  AreaChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function TrafficOverview({
  history = [],
}) {
  const data = useMemo(() => {

    if (
      Array.isArray(history) &&
      history.length
    ) {
      return history
        .slice(-30)
        .map((item, index) => ({
          time:
            item.video_time_seconds ??
            index,
          congestion:
            Number(
              item.congestion_score ?? 0
            ),
          queue:
            Number(
              item.queue_count ?? 0
            ),
          speed:
            Number(
              item.average_speed ?? 0
            ),
        }));
    }

    return [];
  }, [history]);

  return (
    <div className="panel chart-panel">

      <div className="panel-header">

        <div>
          <div className="eyebrow">
            TRAFFIC INTELLIGENCE
          </div>

          <h2>
            Congestion trend
          </h2>
        </div>

        <div className="chart-legend">
          <span>
            <i />
            Congestion
          </span>
        </div>

      </div>

      <div className="chart-container">

        {data.length ? (
          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <AreaChart data={data}>

              <defs>
                <linearGradient
                  id="congestionGradient"
                  x1="0"
                  y1="0"
                  x2="0"
                  y2="1"
                >
                  <stop
                    offset="0%"
                    stopOpacity={0.3}
                  />

                  <stop
                    offset="100%"
                    stopOpacity={0}
                  />
                </linearGradient>
              </defs>

              <XAxis
                dataKey="time"
                tickLine={false}
                axisLine={false}
                tick={{
                  fontSize: 10,
                }}
              />

              <YAxis
                domain={[0, 100]}
                tickLine={false}
                axisLine={false}
                tick={{
                  fontSize: 10,
                }}
              />

              <Tooltip
                contentStyle={{
                  background:
                    "#10151d",
                  border:
                    "1px solid #27313d",
                  borderRadius: 10,
                }}
              />

              <Area
                type="monotone"
                dataKey="congestion"
                strokeWidth={2}
                fill="url(#congestionGradient)"
              />

            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <div className="empty-chart">
            Waiting for traffic history...
          </div>
        )}

      </div>

    </div>
  );
}