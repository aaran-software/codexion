import React from "react";
import ReactDOM from "react-dom/client";
import AppRoutes from "./Routes";
import "../theme.css";
import {BrowserRouter} from "react-router-dom";
import {AppProvider} from "../../global/AppContaxt";
import {AuthProvider} from "../../global/auth/AuthContext";
import settings from "../public/settings.json";
import AppInitializer from "../../global/useSettings";

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
