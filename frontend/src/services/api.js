import axios from "axios";

const api = axios.create({
  baseURL: "https://eduassist-ai-mwj6.onrender.com",
});

export default api;