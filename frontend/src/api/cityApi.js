import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const fetchCities = async () => {
  const response = await axios.get(`${API_BASE}/api/cities`);
  return response.data;
};