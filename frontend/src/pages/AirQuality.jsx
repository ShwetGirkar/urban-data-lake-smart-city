import KpiCards from "../components/kpi/KpiCards";

export default function AirQuality() {

  return (

    <div style={{ padding: "20px" }}>

      <h1>Air Quality Analytics</h1>

      <KpiCards />

      <div style={{ marginTop: "30px" }}>

        <h2>AQI Trend</h2>

        <p>Chart will appear here</p>

      </div>

    </div>

  );

}