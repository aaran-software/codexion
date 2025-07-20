import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./theme.css";
import App from "./App.tsx";

import { AppProvider } from "./pages/GlobalContext/AppContaxt.tsx";
import AppInitializer from "./pages/app/useSettings.tsx";
createRoot(document.getElementById("root")!).render(
    <AppInitializer>
      <AppProvider>
        <StrictMode>
          <App />
        </StrictMode>
      </AppProvider>
    </AppInitializer>
);
