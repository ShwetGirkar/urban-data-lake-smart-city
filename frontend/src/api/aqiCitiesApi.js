import axios from "axios";

const API = "http://127.0.0.1:8000";

export const fetchCityAqi = async () => {
  const res = await axios.get(`${API}/api/cities`);
  return res.data;
};