import {
  useEffect,
  useState,
  createContext,
  useContext,
  type ReactNode,
} from "react";
import { useAppContext } from "./AppContaxt"; // Ensure the file name is correct
const SettingsContext = createContext<any>(null);

export function useAppSettings() {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error("useAppSettings must be used within AppInitializer");
  }
  return context;
}

export default function AppInitializer({ children }: { children: ReactNode }) {
  const [settings, setSettings] = useState<any>(null);
  const { APP_TYPE } = useAppContext();

  useEffect(() => {
    if (!APP_TYPE) return;

    let jsonPath = "/settings.json";
    // switch (APP_CODE) {
    //   case "cortex":
    //     jsonPath = "/settings.json";
    //     break;
    //   case "ecart":
    //     jsonPath = "/menubar.json";
    //     break;
    //   case "mazsone":
    //   case "logicx":
    //     jsonPath = "/JSON/mazsone/menubar.json";
    //     break;
    //   case "cxsun":
    //   default:
    //     jsonPath = "/settings.json";
    //     break;
    // }

    console.debug(`[AppInitializer] APP_CODE = ${APP_TYPE}`);
    console.debug(`[AppInitializer] Loading settings from: ${jsonPath}`);

    const loadSettings = async () => {
      try {
        const res = await fetch(jsonPath);
        if (!res.ok) {
          throw new Error(
            `Failed to load settings: ${res.status} ${res.statusText}`
          );
        }
        const data = await res.json();
        console.debug("[AppInitializer] Settings loaded successfully:", data);
        setSettings(data);
      } catch (error) {
        console.error("[AppInitializer] Error loading settings:", error);
      }
    };

    loadSettings();
  }, [APP_TYPE]);

  if (!settings)
    return <div>Loading settings for <strong>{APP_TYPE}</strong>...</div>;

  return (
    <SettingsContext.Provider value={settings}>
      {children}
    </SettingsContext.Provider>
  );
}
