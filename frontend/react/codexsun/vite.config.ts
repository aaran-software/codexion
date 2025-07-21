import {defineConfig, loadEnv} from 'vite'
import react from '@vitejs/plugin-react-swc'
import * as path from 'path'
import tailwindcss from '@tailwindcss/vite'
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig(({ mode }) => {

  const env = loadEnv(mode, path.resolve(__dirname, '../../../'), '')

  return {
    plugins: [
    react(),
    tailwindcss(),
     visualizer({
      filename: './dist/stats.html',
      open: true, // auto opens in browser
    }),
  ],
    define: {
      'import.meta.env.APP_TYPE': JSON.stringify(env.APP_TYPE),
      'import.meta.env.APP_PORT': JSON.stringify(env.API_PORT),
    },
    resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  }
})