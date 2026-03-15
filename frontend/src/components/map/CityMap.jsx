import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import { useEffect, useState } from "react";
import { fetchCities } from "../../api/cityApi";
import CitySearch from "../search/CitySearch";
import { useRef } from "react";

export default function CityMap() {

  const [cities, setCities] = useState([]);

  const mapRef = useRef(null)

  const indiaBounds = [
    [6.5, 68],
    [37.5, 97]
  ];
  const zoomToCity = (city) => {

  const map = mapRef.current;

  if (!map) return;

  map.setView([city.lat, city.lon], 8);

  setCities((prev) => {

    const exists = prev.find(c => c.city === city.city);

    if (exists) return prev;

    return [...prev, city];

  });

  };


  useEffect(() => {
    const loadCities = async () => {
      const data = await fetchCities();
      setCities(data);
    };

    loadCities();
    }, []);
  const getAQIColor = (aqi) => {
  if (aqi <= 50) return "#22c55e";        // Good (green)
  if (aqi <= 100) return "#ffff00d5";       // Moderate (Yellow)
  if (aqi <= 150) return "#f97416";       // Unhealthy for Sensitive (orange)
  if (aqi <= 200) return "#ef4444";       // Unhealthy (red)
  if (aqi <= 300) return "#8b5cf6";       // Very Unhealthy (purple)
  return "#7f1d1d";                       // Hazardous (maroon)
  };
  return (
  <div>

    {/* Search Bar */}
    <div className="map-header">

    <span>City Map</span>

    <CitySearch onSelectCity={zoomToCity} />

    </div>

    <MapContainer
      center={[22.9734, 78.6569]}
      zoom={5}
      minZoom={5}
      maxBounds={indiaBounds}
      style={{ height: "520px", width: "100%" , borderRadius:"10px"}}
      ref={mapRef}
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
            Urban Stress: {((city.urban_stress_score ?? city.stress_score) * 100).toFixed(0)}%
          </Popup>

        </CircleMarker>
      ))}
    </MapContainer>

  </div>
  );
}