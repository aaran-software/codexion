import React, { Suspense } from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Docs from "../../../apps/ecart/src/docs";
import LoadingScreen from "../../../resources/components/loading/LoadingScreen";

function AppRoutes() {
  return (
    <Suspense fallback={<LoadingScreen image={"/assets/linkagro_logo.jpg"} />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/docs" element={<Docs />} />
      </Routes>
    </Suspense>
  );
}

export default AppRoutes;
