import axios from "axios";

const api = axios.create({
  baseURL: "https://youtube-watch-party-tsln.onrender.com",
});

export default api;