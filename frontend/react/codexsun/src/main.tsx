import React from "react";
import ReactDOM from "react-dom/client";
import "./theme.css";
import AppRouter from "./AppRoutes";
import { AuthProvider } from "./pages/app/auth/AuthContext";
import AppInitializer from "./pages/app/useSettings";
import { AppProvider } from "./pages/GlobalContext/AppContaxt";
import settings from "../public/settings.json"; 

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <AppProvider initialSettings={settings}> {/* ✅ wrap at the top */}
      <AppInitializer>
        <AuthProvider>
          <AppRouter />
        </AuthProvider>
      </AppInitializer>
    </AppProvider>
  </React.StrictMode>
);
