import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend
} from "recharts";

export default function TrafficTrendChart({ data }) {

  return (

    <div style={{ background:"#fff", padding:"20px", borderRadius:"10px" }}>

      <h3>Congestion & Speed — Last 24 Hours</h3>

      <ResponsiveContainer width="100%" height={320}>

        <ComposedChart data={data}>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="timestamp"
            tickFormatter={(time) => {
                const date = new Date(time);
                    return date.getHours().toString().padStart(2, "0") + ":00";
                    }}
                    />

          <YAxis yAxisId="left" />

          <YAxis yAxisId="right" orientation="right" />

          <Tooltip />
          <Legend align="center" verticalAlign="bottom" height={36} />
          <Bar
            yAxisId="left"
            dataKey="congestion_ratio"
            fill="#111"
            name="Cnogestion"
          />

          <Line
            yAxisId="right"
            type="monotone"
            dataKey="current_speed_kmh"
            stroke="#2563eb"
            strokeWidth={3}
            name="Speed (km/h)"
          />

        </ComposedChart>

      </ResponsiveContainer>

    </div>

  );

}