import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const searchCity = async (query) => {
  const response = await axios.get(`${API_BASE}/api/search?query=${encodeURIComponent(query)}`);
  return response.data;
};