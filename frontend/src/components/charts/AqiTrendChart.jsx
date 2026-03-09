import {
  AreaChart,
  Area,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend
} from "recharts";

export default function AqiTrendChart({ data }) {

  // scale AQI for visualization
  const chartData = data.map(d => ({
    ...d,
    aqi_scaled: d.aqi * 25
  }));

  return (

    <div style={{
      background:"#fff",
      padding:"20px",
      borderRadius:"10px",
      marginTop:"25px"
    }}>

      <h3>AQI & PM2.5 — Last 24 Hours</h3>

      <ResponsiveContainer width="100%" height={320}>

        <AreaChart data={chartData}>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="timestamp"
            tickFormatter={(time) => {
              const d = new Date(time);
              return d.getHours().toString().padStart(2,"0")+":00";
            }}
          />

          <YAxis yAxisId="left" />

          <YAxis yAxisId="right" orientation="right" />

          <Tooltip />
          <Legend align="center" verticalAlign="bottom" height={36} />

          {/* AQI area */}
          <Area
            yAxisId="left"
            type="monotone"
            dataKey="aqi_scaled"
            stroke="#2563eb"
            fill="#93c5fd"
            name="AQI"
          />

          {/* PM2.5 line */}
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="pm25"
            stroke="#16a34a"
            strokeWidth={3}
            name="PM2.5"
          />

        </AreaChart>

      </ResponsiveContainer>

    </div>

  );
}