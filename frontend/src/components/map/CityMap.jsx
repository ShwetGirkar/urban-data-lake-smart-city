import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import { useEffect, useState } from "react";
import { fetchCities } from "../../api/cityApi";

export default function CityMap() {

  const [cities, setCities] = useState([]);

  const indiaBounds = [
    [6.5, 68],
    [37.5, 97]
  ];

  useEffect(() => {
    const loadCities = async () => {
      const data = await fetchCities();
      setCities(data);
    };

    loadCities();
  }, []);
  const getAQIColor = (aqi) => {
  if (aqi === 1) return "#22c55e"; // green
  if (aqi === 2) return "#84cc16"; // light green
  if (aqi === 3) return "#eab308"; // yellow
  if (aqi === 4) return "#f97316"; // orange
  return "#ef4444"; // red (5)
    };

  return (
    <MapContainer
      center={[22.9734, 78.6569]}
      zoom={5}
      minZoom={5}
      maxBounds={indiaBounds}
      style={{ height: "500px", width: "100%" }}
    >

    <TileLayer
      attribution="© OpenStreetMap"
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    />

    {cities.map((city, index) => (
      <CircleMarker
                    key={index}
                    center={[city.lat, city.lon]}
                    radius={10}
                    pathOptions={{
                      color: getAQIColor(city.aqi),
                      fillColor: getAQIColor(city.aqi),
                      fillOpacity: 0.8
                    }}
                  >
          <Popup>
            <strong>{city.city}</strong>
            <br />
            AQI: {city.aqi}
            <br />
            Congestion: {(city.congestion_ratio * 100).toFixed(0)}%
            <br />
            Urban Stress: {(city.urban_stress_score * 100).toFixed(0)}%
          </Popup>
        </CircleMarker>
      ))}

    </MapContainer>
    );
}