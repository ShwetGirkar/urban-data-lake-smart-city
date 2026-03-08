import axios from "axios";

const API = "http://127.0.0.1:8000";

export const fetchAlerts = async () => {
  const res = await axios.get(`${API}/api/alerts`);
  return res.data;
};