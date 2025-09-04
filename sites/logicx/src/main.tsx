import React from "react";
import ReactDOM from "react-dom/client";
import "../theme.css";
import {BrowserRouter} from "react-router-dom";
import settings from "../public/settings.json";
import AppRoutes from "./Routes";
import {AppProvider} from "../../../resources/global/AppContaxt";
import {AuthProvider} from "../../../resources/global/auth/AuthContext";
import AppInitializer from "../../../resources/global/useSettings";

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
