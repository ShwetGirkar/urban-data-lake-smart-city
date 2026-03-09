import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const fetchTrafficTrend = async (city) => {

  const response = await axios.get(`${API_BASE}/api/traffic/${city}`);

  return response.data;

};