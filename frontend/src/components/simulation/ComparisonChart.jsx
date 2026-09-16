import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const data = [
  {
    metric: "Waiting",
    fixed: 48,
    flowmind: 31,
  },
  {
    metric: "Queue",
    fixed: 72,
    flowmind: 43,
  },
  {
    metric: "Congestion",
    fixed: 78,
    flowmind: 54,
  },
];

export default function ComparisonChart() {
  return (
    <div className="panel">

      <div className="panel-header">

        <div>
          <div className="eyebrow">
            STRATEGY COMPARISON
          </div>

          <h2>
            Fixed vs FlowMind
          </h2>
        </div>

      </div>

      <div className="comparison-chart">

        <ResponsiveContainer
          width="100%"
          height="100%"
        >
          <BarChart data={data}>

            <CartesianGrid
              vertical={false}
              strokeOpacity={0.1}
            />

            <XAxis
              dataKey="metric"
              axisLine={false}
              tickLine={false}
            />

            <YAxis
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

            <Bar
              dataKey="fixed"
              name="Fixed"
              radius={[5, 5, 0, 0]}
            />

            <Bar
              dataKey="flowmind"
              name="FlowMind"
              radius={[5, 5, 0, 0]}
            />

          </BarChart>
        </ResponsiveContainer>

      </div>

    </div>
  );
}