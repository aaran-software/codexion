import axios from 'axios';

// const apiMethod = import.meta.env.VITE_API_METHOD || 'FAST_API';
const appType = (import.meta.env.VITE_APP_TYPE || 'cxsun').toUpperCase();

// ✅ Dynamically access base URL and token from env
const env = import.meta.env;
const apiMethod = env[`VITE_${appType}_API_METHOD`] || 'FAST_API';
const baseURL = env[`VITE_${appType}_API_URL`] || env.VITE_API_URL;
const frappeToken = env[`VITE_${appType}_TOKEN`];

const apiClient = axios.create({
  baseURL,
  withCredentials: true,
});

apiClient.interceptors.request.use(
  (config) => {
    if (apiMethod === 'FRAPPE') {
      // ✅ Use dynamic Frappe token based on APP_TYPE
      if (frappeToken) {
        config.headers['Authorization'] = frappeToken;
        config.headers['Content-Type'] = 'application/json';
      }else{
          alert("Token Missing")
      }
    } else {
      // ✅ FAST_API: Token from localStorage
      const token = localStorage.getItem('token');
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export default apiClient;

// import axios from "axios";

// const appType = (import.meta.env.VITE_APP_TYPE || "cxsun").toUpperCase();
// const env = import.meta.env;
// const apiMethod = env[`VITE_${appType}_API_METHOD`] || "FAST_API";
// const baseURL = env[`VITE_${appType}_API_URL`] || env.VITE_API_URL;

// // API client without static token in header
// const apiClient = axios.create({
//   baseURL,
//   withCredentials: true,
// });

// // Function to set token dynamically
// export function setFrappeToken(token: string | null) {
//   if (token) {
//     apiClient.defaults.headers.common["Authorization"] = `token ${token}`;
//     apiClient.defaults.headers.common["Content-Type"] = "application/json";
//   } else {
//     delete apiClient.defaults.headers.common["Authorization"];
//   }
// }

// // Interceptor for FAST_API tokens stored in localStorage
// apiClient.interceptors.request.use(
//   (config) => {
//     if (apiMethod === "FAST_API") {
//       const token = localStorage.getItem("token");
//       if (token) {
//         config.headers["Authorization"] = `Bearer ${token}`;
//       }
//     }
//     // Do not set frappeToken here - manage explicitly
//     return config;
//   },
//   (error) => Promise.reject(error)
// );

// export default apiClient;
