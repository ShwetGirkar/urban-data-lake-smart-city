export default function AqiPrediction({ data }) {

  if (!data) return null;

  return (

    <div style={{
      background:"#fff",
      padding:"20px",
      borderRadius:"10px",
      marginTop:"25px"
    }}>

      <h3>AQI Prediction</h3>

      <p><strong>Latest AQI:</strong> {data.latest_aqi}</p>

      <p><strong>Predicted AQI:</strong> {data.predicted_aqi}</p>

      <p><strong>Risk Level:</strong> {data.risk_level}</p>

      <p><strong>Alert:</strong> {data.alert}</p>

    </div>

  );

}