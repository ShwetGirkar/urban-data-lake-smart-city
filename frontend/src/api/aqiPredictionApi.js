import axios from "axios";

const API = "http://127.0.0.1:8000";

export const fetchAqiPrediction = async (city) => {

  const res = await axios.get(`${API}/api/predict/aqi/${city}`);

  return res.data;

};