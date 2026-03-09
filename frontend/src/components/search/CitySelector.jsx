export default function CitySelector({ cities, selectedCity, onChange }) {

  return (

    <div style={{ marginBottom: "20px" }}>

      <label>Select City: </label>

      <select
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