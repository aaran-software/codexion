import {
    createContext,
    useContext,
    useEffect,
    useState,
    type ReactNode,
} from "react";

type Settings = {
    theme: string;
    recordsPerPage: number;
    // Add more fields as needed
};

type AppContextType = {
    currentComponent: string;
    setCurrentComponent: (name: string) => void;

    settings: Settings | null;
    updateSettings: (newSettings: Partial<Settings>) => void;
    APP_CODE: string; // Expose APP_CODE to the context
    API_URL: string; // Expose API_URL to the context
};

const APP_CODE = import.meta.env.APP_TYPE || 'ecart'
const API_URL = import.meta.env.API_URL || 'http://127.0.0.1:4000'

// console.log(APP_CODE)

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider = ({children}: { children: ReactNode }) => {
    const [currentComponent, setCurrentComponent] = useState("");
    const [settings, setSettings] = useState<Settings | null>(null);

    // Load settings from /settings.json (public folder)
    useEffect(() => {
        const saved = localStorage.getItem("user_settings");
        if (saved) {
            setSettings(JSON.parse(saved));
        } else {
            fetch("/settings.json")
                .then((res) => res.json())
                .then((data) => {
                    setSettings(data);
                    localStorage.setItem("user_settings", JSON.stringify(data));
                })
                .catch((err) => console.error("Failed to load settings:", err));
        }
    }, []);

    const updateSettings = (newSettings: Partial<Settings>) => {
        setSettings((prev) => {
            if (!prev) return prev;
            const updated = {...prev, ...newSettings};
            localStorage.setItem("user_settings", JSON.stringify(updated));
            return updated;
        });
    };

    return (
        <AppContext.Provider
            value={{
                currentComponent,
                setCurrentComponent,
                settings,
                updateSettings,
                APP_CODE, // Expose APP_CODE to the context
                API_URL, // Expose APP_CODE to the context
            }}
        >
            {children}
        </AppContext.Provider>
    );
};

export const useAppContext = () => {
    const context = useContext(AppContext);
    if (!context) {
        throw new Error("useAppContext must be used within AppProvider");
    }
    return context;
};
