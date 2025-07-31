import axios from "axios";

const frappeBaseApi = axios.create({
  baseURL: "https://dev.aaranerp.com/",
  withCredentials: true,
});

frappeBaseApi.interceptors.request.use(
  (config) => {
    const token = "token 952cb80a43294ad:664a957650e7386";
    if (token) {
      config.headers["Authorization"] = token;
      config.headers["Content-Type"] = "application/json";
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default frappeBaseApi;
