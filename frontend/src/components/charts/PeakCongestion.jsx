export default function PeakCongestion({ data }) {

  // Sort by congestion descending
  const sortedData = [...data].sort(
    (a, b) => b.congestion_ratio - a.congestion_ratio
  );

  return (

    <div className="panel">

      <h3 className="panel-title">Peak Congestion (Top 5 Hours)</h3>

      {sortedData.map((item, index) => {

        const date = new Date(item.timestamp);
        const hour = date.getHours().toString().padStart(2, "0");

        return (

      <div key={index} className="peak-row">

      <span className="peak-time">{hour}:00</span>

        <div className="peak-bar-wrapper">

        <div
          className="peak-bar"
          style={{
          width: `${item.congestion_ratio * 100}%`
          }}
          ></div>

          </div>

        <span className="peak-value">
            {(item.congestion_ratio * 100).toFixed(0)}%
        </span>

      </div>

        );

      })}

    </div>

  );
}