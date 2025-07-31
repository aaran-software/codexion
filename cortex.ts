// -------------------------------
// 🔧 Vite Config for Backend Assets (Tailwind for Jinja2 templates)
// -------------------------------

import { defineConfig } from 'vite'
import path from 'path'

export default defineConfig({
  root: path.resolve(__dirname, 'backend'),

  css: {
    postcss: path.resolve(__dirname, 'postcss.config.js') // Load PostCSS config
  },

  build: {
    outDir: path.resolve(__dirname, 'public/backend/build'),
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'resources/css/app.css'),
        script: path.resolve(__dirname, 'resources/js/app.ts'),
      },
    },
  },
})