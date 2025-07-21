// main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import "./theme.css";
import AppRouter from "./AppRoutes";
import { AppProvider } from "./pages/GlobalContext/AppContaxt";
import AppInitializer from "./pages/app/useSettings";
import { AuthProvider } from "./pages/app/auth/AuthContext";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <AppProvider>
      <AuthProvider>
        <AppInitializer> {/* ✅ Wrap with this */}
            <AppRouter />
        </AppInitializer>
      </AuthProvider>
    </AppProvider>
  </React.StrictMode>
);
