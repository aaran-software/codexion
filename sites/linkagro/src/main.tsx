import React from "react";
import ReactDOM from "react-dom/client";
import "../theme.css";
import 'animate.css';

import {BrowserRouter} from "react-router-dom";
import settings from "../public/settings.json";
import AppRoutes from "./Routes";
import {AppProvider} from "../../../resources/global/AppContaxt";
import {AuthProvider} from "../../../resources/global/auth/AuthContext";
import AppInitializer from "../../../resources/global/useSettings";
import {ThemeProvider} from "../../../resources/global/theme-provider";
ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
       <ThemeProvider defaultTheme="light">
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
