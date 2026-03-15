import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  BarChart,
  Legend
} from "recharts";

export default function AqiCityChart({ data }) {
    const chartData = data.map(d => ({
    ...d,
    aqi_real: d.aqi 
    }));

  return (

    <div className="panel">

      <h3 className="panel-title">AQI Trend Across Cities</h3>

      <ResponsiveContainer width="100%" height={300}>

        <LineChart data={chartData}>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="city" stroke="#ffffff" />

          <YAxis domain={[0,500]} stroke="#ffffff" />

          <Tooltip
            contentStyle={{
            background:"#1e293b",
            border:"1px solid #334155",
            color:"#fff"
                }}
          />
          <Legend align="center" verticalAlign="bottom" height={36} />
          <Line
            type="monotone"
            dataKey="aqi_real"
            stroke="#ef4444"
            strokeWidth={3}
            name="AQI Trend Line (Across citys)"
          />

        </LineChart>

      </ResponsiveContainer>

    </div>

  );

}