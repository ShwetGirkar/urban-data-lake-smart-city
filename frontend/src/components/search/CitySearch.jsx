import { useState } from "react";
import { searchCity } from "../../api/searchApi";

export default function CitySearch({ onSelectCity }) {

  const [query, setQuery] = useState("");

    const handleSearch = async () => {

    if (!query) return;

    try {

        const result = await searchCity(query);

    const city = {
    city: result.data.city || result.data.location,
    lat: result.data.lat,
    lon: result.data.lon,
    aqi: result.data.aqi,
    congestion_ratio: result.data.congestion_ratio,
    urban_stress_score:
        result.data.urban_stress_score ?? result.data.stress_score
    };

    onSelectCity(city);

  } catch (error) {

    console.error("Search failed", error);

  }

    };

  return (

    <div style={{ marginBottom: "10px" }}>

      <input
        type="text"
        placeholder="Search city..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button onClick={handleSearch}>
        Search
      </button>

    </div>

  );
}