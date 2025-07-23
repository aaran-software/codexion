import React from "react";
import { Routes, Route } from "react-router-dom";
import App from "./App";
import Service from "./service";

function AppRoutes() {
  return (
    <Routes>
      {/* <App /> */}
      <Route path="/service" element={<Service />} />
      <Route path="/" element={<App />} />
    </Routes>
  );
}

export default AppRoutes;
