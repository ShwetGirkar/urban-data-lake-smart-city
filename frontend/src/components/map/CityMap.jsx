import { MapContainer, TileLayer } from "react-leaflet";

export default function CityMap() {

  const indiaBounds = [
    [6.5, 68],   // southwest
    [37.5, 97]   // northeast
  ];

  return (
    <MapContainer
      center={[22.9734, 78.6569]}
      zoom={5}
      minZoom={5}
      maxZoom={7}
      maxBounds={indiaBounds}
      style={{ height: "500px", width: "100%" }}
    >
      <TileLayer
        attribution="© OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
    </MapContainer>
  );
}