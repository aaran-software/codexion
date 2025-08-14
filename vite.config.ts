import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react-swc";
import * as path from "path";

export default defineConfig(({ mode }) => {
  // ✅ Load env from project root
  const env = loadEnv(mode, process.cwd(), "");

  const appName = env.VITE_APP_TYPE || "cxsun";
  const appCategory = env.VITE_APP_CATEGORY || "apps";

  const appRoot = path.resolve(__dirname, `${appCategory}/${appName}`);
  const appSrc = path.resolve(appRoot, "src");

  // ✅ Pick all VITE_ envs for frontend use
  const viteEnvVars = Object.keys(env)
    .filter((key) => key.startsWith("VITE_"))
    .reduce(
      (acc, key) => {
        acc[`import.meta.env.${key}`] = JSON.stringify(env[key]);
        return acc;
      },
      {} as Record<string, string>
    );

  // ✅ Read ALLOWED_HOST from .env, fallback to 'localhost'
  const allowedHost = env.ALLOWED_HOST || "localhost";

  return {
    root: appRoot,
    plugins: [react()],
    resolve: {
      alias: {
        "@": appSrc,
        "@resources": path.resolve(__dirname, "resources"),
      },
    },
    define: {
      ...viteEnvVars,
    },
    build: {
      outDir: path.resolve(__dirname, "public/build"),
      emptyOutDir: true,
      manifest: true,
    },
    server: {
      port: Number(env.APP_PORT) || 3005,
      host: true, // binds to 0.0.0.0
      allowedHosts: [allowedHost],
      hmr: {
        host: allowedHost,
        protocol: env.APP_HTTPS === "true" ? "wss" : "ws",
        port: Number(env.APP_PORT) || 3005,
      },
    },
  };
});