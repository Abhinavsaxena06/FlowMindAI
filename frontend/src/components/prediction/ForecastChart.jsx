import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function ForecastChart({
  current = 0,
  predicted = [],
}) {
  const data = [
    {
      time: "Now",
      value: Number(current),
    },
    ...predicted,
  ];

  return (
    <div className="panel">

      <div className="panel-header">

        <div>
          <div className="eyebrow">
            FORECAST
          </div>

          <h2>
            Congestion outlook
          </h2>
        </div>

      </div>

      <div className="forecast-chart">

        <ResponsiveContainer
          width="100%"
          height="100%"
        >
          <LineChart data={data}>

            <XAxis
              dataKey="time"
              axisLine={false}
              tickLine={false}
            />

            <YAxis
              domain={[0, 100]}
              axisLine={false}
              tickLine={false}
            />

            <Tooltip
              contentStyle={{
                background:
                  "#0A1020",
                border:
                  "1px solid #24344D",
                borderRadius: 10,
                color: "#F8FAFC",
              }}
            />

            <Line
              type="monotone"
              dataKey="value"
              strokeWidth={3}
              dot={{
                r: 4,
              }}
            />

          </LineChart>
        </ResponsiveContainer>

      </div>

    </div>
  );
}