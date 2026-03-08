import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const fetchSummary = async () => {
  const response = await axios.get(`${API_BASE}/api/summary`);
  return response.data;
};