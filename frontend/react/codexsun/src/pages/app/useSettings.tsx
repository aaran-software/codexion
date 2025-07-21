// import { useEffect, useState, createContext, useContext, type ReactNode } from "react";

// // Create context
// const SettingsContext = createContext<any>(null);

// // Custom hook to access settings
// export function useAppSettings() {
//   const context = useContext(SettingsContext);
//   if (!context) {
//     throw new Error("useAppSettings must be used within AppInitializer");
//   }
//   return context;
// }

// // Provider component that loads settings and provides them via context
// export default function AppInitializer({ children, }: { children: ReactNode }) {
//   const [settings, setSettings] = useState<any>(null);

//   // const [jsonPath,setJsonPath]=useState("web");
//   // const {APP_CODE}=useAppContext()

//   // if(APP_CODE==="web"){
//   //   setJsonPath("/settings.json")
//   // }else{
//   //   setJsonPath("/settings.json")

//   // }
//   useEffect(() => {
//     async function loadSettings() {
//       try {
//         const res = await fetch("/settings.json");
//         const data = await res.json();
//         setSettings(data);
//       } catch (error) {
//         console.error("Failed to load settings.json", error);
//       }
//     }

//     loadSettings();
//   }, []);

//   if (!settings) return <div>Loading settings...</div>;

//   return (
//     <SettingsContext.Provider value={settings}>
//       {children}
//     </SettingsContext.Provider>
//   );
// }


import {
  useEffect,
  useState,
  createContext,
  useContext,
  type ReactNode,
} from "react";
import { useAppContext } from "../GlobalContext/AppContaxt";

// Create context
const SettingsContext = createContext<any>(null);

// Hook to access settings
export function useAppSettings() {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error("useAppSettings must be used within AppInitializer");
  }
  return context;
}

// 👇 Dummy AppContext (replace this with your real one)
// function useAppContext() {
//   // Example mockup – replace with real app code
//   return { APP_CODE: "web2" }; // can be "web", "admin", etc.
// }

// Provider that loads settings dynamically based on APP_CODE
export default function AppInitializer({ children }: { children: ReactNode }) {
  const { APP_CODE } = useAppContext(); // Get app code from context
  console.log(APP_CODE)
  const [settings, setSettings] = useState<any>(null);

  useEffect(() => {
    async function loadSettings() {
      try {
        // Determine path based on APP_CODE
        const jsonPath = APP_CODE === "billing"
          ? "/settings.json"
          : APP_CODE === "web2"
          ? "/JSON/codexsun/menubar.json"
          : "/settings.json";

        const res = await fetch(jsonPath);
        const data = await res.json();
        setSettings(data);
      } catch (error) {
        console.error("Failed to load settings file:", error);
      }
    }

    loadSettings();
  }, [APP_CODE]);

  if (!settings) return <div>Loading settings...</div>;

  return (
    <SettingsContext.Provider value={settings}>
      {children}
    </SettingsContext.Provider>
  );
}
