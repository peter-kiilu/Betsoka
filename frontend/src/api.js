import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api",
});

export const getStatus = () => API.get("/status");
export const getFeatures = () => API.get("/features");
export const generateData = (n_matches) => API.post("/generate", { n_matches });
export const trainModels = () => API.post("/train");
export const predictOutcome = (data) => API.post("/predict", data);

export default API;
