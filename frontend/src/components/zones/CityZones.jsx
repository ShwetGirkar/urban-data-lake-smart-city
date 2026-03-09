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
    return "#f35060";
  };

  return (
    <div style={{ marginTop: "40px" }}>

      <h2 style={{ marginBottom: "20px" }}>
        City Zones – AQI vs Congestion
      </h2>

      <div className="zones-grid">

        {cities.map((city, index) => (

          <div
            key={index}
            className="zone-card"
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
                background: getRiskColor(city.risk_level),
                color: "#fff"
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
                  background: "#db2222",
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