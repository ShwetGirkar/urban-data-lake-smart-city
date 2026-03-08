import { useEffect, useState } from "react";
import axios from "axios";

export default function CityZones() {

  const [cities, setCities] = useState([]);

  useEffect(() => {
    fetchCities();
  }, []);

  const fetchCities = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/cities");
      setCities(res.data);
    } catch (err) {
      console.error("Failed to fetch city zones", err);
    }
  };

  const getRiskColor = (risk) => {
    if (risk === "Good") return "#28a745";
    if (risk === "Satisfactory") return "#17a2b8";
    if (risk === "Moderate") return "#ffc107";
    return "#dc3545";
  };

  return (
    <div style={{ marginTop: "40px" }}>

      <h2 style={{ marginBottom: "20px" }}>
        City Zones – AQI vs Congestion
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
          gap: "16px"
        }}
      >

        {cities.map((city, index) => (

          <div
            key={index}
            style={{
              background: "#fff",
              padding: "16px",
              borderRadius: "10px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.1)"
            }}
          >

            <h4>{city.city}</h4>

            {/* AQI */}
            <div style={{ marginTop: "6px" }}>
              AQI <strong>{city.aqi}</strong>

              <span
                style={{
                  marginLeft: "8px",
                  padding: "2px 8px",
                  borderRadius: "6px",
                  fontSize: "12px",
                  background: "#eee"
                }}
              >
                {city.risk_level}
              </span>
            </div>

            {/* Congestion */}
            <div style={{ marginTop: "10px" }}>
              Congestion {Math.round(city.congestion_ratio * 100)}%
            </div>

            {/* Progress Bar */}
            <div
              style={{
                marginTop: "6px",
                height: "8px",
                background: "#eee",
                borderRadius: "5px"
              }}
            >
              <div
                style={{
                  width: `${city.congestion_ratio * 100}%`,
                  height: "100%",
                  background: "#1f2937",
                  borderRadius: "5px"
                }}
              />
            </div>

          </div>

        ))}

      </div>

    </div>
  );
}