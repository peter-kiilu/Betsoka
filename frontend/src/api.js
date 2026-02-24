import axios from "axios";

// In production (same origin), use relative path. In dev, use localhost:8000
const baseURL = import.meta.env.DEV
  ? "http://localhost:8000/api"
  : "/api";

const API = axios.create({ baseURL });

export const getStatus = () => API.get("/status");
export const getFeatures = () => API.get("/features");
export const generateData = (n_matches) => API.post("/generate", { n_matches });
export const trainModels = () => API.post("/train");
export const predictOutcome = (data) => API.post("/predict", data);

export default API;
