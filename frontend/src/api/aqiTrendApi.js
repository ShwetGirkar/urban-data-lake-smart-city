import axios from "axios";

const API = "http://127.0.0.1:8000";

export const fetchAqiTrend = async (city) => {

  const res = await axios.get(`${API}/api/air-quality/${city}`);

  return res.data;

};