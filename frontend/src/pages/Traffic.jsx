import { useEffect, useState } from "react";
import KpiCards from "../components/kpi/KpiCards";
import TrafficTrendChart from "../components/charts/TrafficTrendChart";
import CitySelector from "../components/search/CitySelector";
import { fetchTrafficTrend } from "../api/trafficTrendApi";
import PeakCongestion from "../components/charts/PeakCongestion";

export default function Traffic() {

  const [trend, setTrend] = useState([]);
  const [peakHours, setPeakHours] = useState([]);

  const [city, setCity] = useState("Mumbai");

  const cities = [
    "Mumbai","Delhi","Bengaluru","Chennai","Kolkata","Hyderabad",
    "Pune","Ahmedabad","Jaipur","Indore","Bhopal","Nagpur",
    "Lucknow","Kanpur","Patna","Ranchi","Bhubaneswar"
  ];

  useEffect(() => {

    const loadData = async () => {

    const data = await fetchTrafficTrend(city);

      setTrend(data.traffic_trend);
      setPeakHours(data.peak_hours);

    };

    loadData();

  }, [city]);

  return (

    <div style={{ padding:"20px" }}>

      <h1>Traffic Analytics</h1>

      <KpiCards />

      <CitySelector
        cities={cities}
        selectedCity={city}
        onChange={setCity}
      />

      <TrafficTrendChart data={trend} />
      <PeakCongestion data={peakHours} />

    </div>

  );

}