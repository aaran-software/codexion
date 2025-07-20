import {defineConfig, loadEnv} from 'vite'
import react from '@vitejs/plugin-react-swc'
import * as path from 'path'

export default defineConfig(({ mode }) => {

  const env = loadEnv(mode, path.resolve(__dirname, '../../../'), '')

  return {
    plugins: [react()],
    define: {
      'import.meta.env.APP_TYPE': JSON.stringify(env.APP_TYPE),
    },
  }
})