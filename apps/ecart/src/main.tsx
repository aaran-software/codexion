import React from "react";
import ReactDOM from "react-dom/client";
import "../theme.css";
import {BrowserRouter} from "react-router-dom";
import {AppProvider} from "../../global/AppContaxt";
import {AuthProvider} from "../../global/auth/frappeAuthContext";
import settings from "../public/settings.json";
import AppInitializer from "../../global/useSettings";
import AppRoutes from "./Routes";

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <BrowserRouter>
            <AppProvider initialSettings={settings}>
                <AuthProvider> {/* ✅ Add this wrapper */}
                    <AppInitializer>
                        <AppRoutes/>
                    </AppInitializer>
                </AuthProvider>
            </AppProvider>
        </BrowserRouter>
    </React.StrictMode>
);
