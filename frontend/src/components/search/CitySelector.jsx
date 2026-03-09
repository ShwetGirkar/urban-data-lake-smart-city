export default function CitySelector({ cities, selectedCity, onChange }) {

  return (

    <div className="city-selector">

      <label className="city-label">Select City</label>

      <select
        className="city-dropdown"
        value={selectedCity}
        onChange={(e) => onChange(e.target.value)}
      >
        {cities.map((city, index) => (
          <option key={index} value={city}>
            {city}
          </option>
        ))}
      </select>

    </div>

  );

}