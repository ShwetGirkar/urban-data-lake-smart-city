import { useEffect, useState } from "react";
import axios from "axios";

export default function UrbanStressPanel() {

  const [cities, setCities] = useState([]);

  useEffect(() => {
    fetchStressCities();
  }, []);

  const fetchStressCities = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/predict/stress-ranking");
      setCities(res.data);
    } catch (err) {
      console.error("Failed to fetch urban stress data", err);
    }
  };

  return (
    <div style={{
      background: "#ffffff",
      padding: "16px",
      borderRadius: "10px",
      boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
      height: "500px"
    }}>

      <h3 style={{ marginBottom: "16px" }}>
        Top Urban Stress Cities
      </h3>

      {cities.map((city, index) => (

        <div key={index}
          style={{
            marginBottom: "14px",
            padding: "10px",
            border: "1px solid #eee",
            borderRadius: "8px"
          }}
        >

         <div style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center"
            }}>

        <strong>{city.city}</strong>

        <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>

        <span>{Math.round(city.stress_index * 100)}%</span>

        <span
        style={{
            padding: "3px 8px",
            borderRadius: "6px",
            fontSize: "12px",
            fontWeight: "500",
            background:
            city.level === "Low"
                ? "#d4edda"
                : city.level === "Moderate"
                ? "#ffeeba"
                : "#f8d7da",
            color:
            city.level === "Low"
                ? "#155724"
                : city.level === "Moderate"
                ? "#856404"
                : "#721c24"
        }}
        >
        {city.level}
        </span>

    </div>

    </div>
          {/* Progress Bar */}
          <div style={{
            height: "8px",
            background: "#eee",
            borderRadius: "5px",
            marginTop: "6px"
          }}>
            <div style={{
              width: `${city.stress_index * 100}%`,
              height: "100%",
              background: "#ff6b6b",
              borderRadius: "5px"
            }} />
          </div>

        </div>

      ))}

    </div>
  );
}