import {
  useEffect,
  useState,
  createContext,
  useContext,
  type ReactNode,
} from "react";
import { useAppContext } from "../GlobalContext/AppContaxt";

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
  const { APP_CODE } = useAppContext();

  useEffect(() => {
    if (!APP_CODE) return;

    const jsonPath =
      APP_CODE === "billing"
        ? "/settings.json"
        : APP_CODE === "cortex"
        ? "/JSON/codexsun/menubar.json"
        : APP_CODE === "ecart"
        ? "/JSON/ecart/menubar.json"
        : APP_CODE === "mazsone"
        ? "/JSON/mazsone/menubar.json"
        : APP_CODE === "logicx"
        ? "/JSON/mazsone/menubar.json"
        : "/settings.json";

    const loadSettings = async () => {
      try {
        const res = await fetch(jsonPath);
        if (!res.ok) throw new Error(`Failed to load settings from ${jsonPath}`);
        const data = await res.json();
        setSettings(data);
      } catch (error) {
        console.error("Error loading settings:", error);
      }
    };

    loadSettings();
  }, [APP_CODE]);

  if (!settings) return <div>Loading settings for {APP_CODE}...</div>;

  return (
    <SettingsContext.Provider value={settings}>
      {children}
    </SettingsContext.Provider>
  );
}
