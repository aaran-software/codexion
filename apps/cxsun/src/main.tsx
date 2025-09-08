import React from "react";
import ReactDOM from "react-dom/client";
import AppRoutes from "./Routes";
import "../theme.css";
import {BrowserRouter} from "react-router-dom";
import {AppProvider} from "../../../resources/global/AppContaxt";
import {AuthProvider} from "../../../resources/global/auth/AuthContext";
import settings from "../public/settings.json";
import AppInitializer from "../../../resources/global/useSettings";
import {ThemeProvider} from "../../../resources/global/theme-provider";

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <ThemeProvider defaultTheme="system">
            <BrowserRouter>
            <AppProvider initialSettings={settings}>
                <AuthProvider> {/* ✅ Add this wrapper */}
                    <AppInitializer>
                        <AppRoutes/>
                    </AppInitializer>
                </AuthProvider>
            </AppProvider>
        </BrowserRouter>
        </ThemeProvider>

    </React.StrictMode>
);
