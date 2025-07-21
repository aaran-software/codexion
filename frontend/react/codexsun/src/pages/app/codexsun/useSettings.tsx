import { useEffect, useState, createContext, useContext, type ReactNode } from "react";

// Create context
const SettingsContext = createContext<any>(null);

// Custom hook to access settings
export function useAppSettings() {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error("useAppSettings must be used within AppInitializer");
  }
  return context;
}

// Provider component that loads settings and provides them via context
export default function AppInitializer({ children }: { children: ReactNode }) {
  const [settings, setSettings] = useState<any>(null);

  useEffect(() => {
    async function loadSettings() {
      try {
        const res = await fetch("/settings.json");
        const data = await res.json();
        setSettings(data);
      } catch (error) {
        console.error("Failed to load settings.json", error);
      }
    }

    loadSettings();
  }, []);

  if (!settings) return <div>Loading settings...</div>;

  return (
    <SettingsContext.Provider value={settings}>
      {children}
    </SettingsContext.Provider>
  );
}
