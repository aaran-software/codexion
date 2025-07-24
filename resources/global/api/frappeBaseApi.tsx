import axios from "axios";

const frappeBaseApi = axios.create({
  baseURL: "https://dev.aaranerp.com/",
  withCredentials: true,
});

frappeBaseApi.interceptors.request.use(
  (config) => {
    const token = "token 8e530899aabab95:3849b71bc4a019d";
    if (token) {
      config.headers["Authorization"] = token;
      config.headers["Content-Type"] = "application/json";
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default frappeBaseApi;
