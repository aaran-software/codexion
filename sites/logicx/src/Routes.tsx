import React, { Suspense } from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Docs from "../../../apps/ecart/src/docs";
import LoadingScreen from "../../../resources/components/loading/LoadingScreen";
import NotFound from "../../../resources/components/notfound/NotFound";

function AppRoutes() {
  return (
    <Suspense fallback={<LoadingScreen image={"/assets/linkagro_logo.jpg"} />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/docs" element={<Docs />} />
        <Route
          path="*"
          element={
            <NotFound
              title="Oops! Page not found"
              description="The page you are looking for might have been moved or deleted."
              buttonLabel="Back to Home"
              homePath="/"
              highlightColor="text-red-500"
            />
          }
        />
      </Routes>
    </Suspense>
  );
}

export default AppRoutes;
