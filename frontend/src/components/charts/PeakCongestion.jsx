export default function PeakCongestion({ data }) {

  // Sort by congestion descending
  const sortedData = [...data].sort(
    (a, b) => b.congestion_ratio - a.congestion_ratio
  );

  return (

    <div
      style={{
        background: "#fff",
        padding: "20px",
        borderRadius: "10px",
        marginTop: "25px"
      }}
    >

      <h3>Peak Congestion (Top 5 Hours)</h3>

      {sortedData.map((item, index) => {

        const date = new Date(item.timestamp);
        const hour = date.getHours().toString().padStart(2, "0");

        return (

          <div
            key={index}
            style={{
              display: "flex",
              justifyContent: "space-between",
              padding: "8px 0",
              borderBottom: "1px solid #eee"
            }}
          >

            <span>{hour}:00</span>

            <strong>
              {(item.congestion_ratio * 100).toFixed(0)}%
            </strong>

          </div>

        );

      })}

    </div>

  );
}