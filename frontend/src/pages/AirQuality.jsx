import { useEffect, useState } from "react";
import KpiCards from "../components/kpi/KpiCards";
import AqiTrendChart from "../components/charts/AqiTrendChart";
import AqiPrediction from "../components/panels/AqiPrediction";
import CitySelector from "../components/search/CitySelector";
import { fetchAqiTrend } from "../api/aqiTrendApi";
import { fetchAqiPrediction } from "../api/aqiPredictionApi";
import { fetchCityAqi } from "../api/aqiCitiesApi";
import AqiCityChart from "../components/charts/AqiCityChart";

export default function AirQuality() {

  const [cityAqi, setCityAqi] = useState([]);

  const [trend, setTrend] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [city, setCity] = useState("Mumbai");

  const cities = [
    "Mumbai","Delhi","Bengaluru","Chennai","Kolkata","Hyderabad",
    "Pune","Ahmedabad","Jaipur","Indore","Bhopal","Nagpur",
    "Lucknow","Kanpur","Patna","Ranchi","Bhubaneswar"
  ];
  useEffect(() => {

  const loadCityAqi = async () => {
    const data = await fetchCityAqi();
    setCityAqi(data);
  };

  loadCityAqi();

  }, []);
  useEffect(() => {

    const loadData = async () => {

      const trendData = await fetchAqiTrend(city);
      const predData = await fetchAqiPrediction(city);

      setTrend(trendData.aqi_trend);
      setPrediction(predData);

    };

    loadData();

  }, [city]);

  return (

    <div style={{ padding:"20px" }}>

      <h1>Air Quality Analytics</h1>

      <KpiCards />

      <AqiCityChart data={cityAqi} />

      <CitySelector
        cities={cities}
        selectedCity={city}
        onChange={setCity}
      />
      <AqiTrendChart data={trend} />

      <AqiPrediction data={prediction} />

    </div>

  );

}