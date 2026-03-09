export default function AqiPrediction({ data }) {

  if (!data) return null;

  return (

    <div className="panel">

      <h3 className="panel-title">AQI Prediction</h3>

      <div className="prediction-grid">

        <div className="prediction-card">
          <div className="prediction-title">Latest AQI</div>
          <div className="prediction-value">{data.latest_aqi}</div>
        </div>

        <div className="prediction-card">
          <div className="prediction-title">Predicted AQI</div>
          <div className="prediction-value">{data.predicted_aqi}</div>
        </div>

        <div className="prediction-card">
          <div className="prediction-title">Risk Level</div>
          <div className="prediction-value">{data.risk_level}</div>
        </div>

        <div className="prediction-card">
          <div className="prediction-title">Alert</div>
          <div className="prediction-value">{data.alert}</div>
        </div>

      </div>

    </div>

  );

}