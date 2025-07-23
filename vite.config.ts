// vite.config.ts
import {defineConfig, loadEnv} from 'vite'
import react from '@vitejs/plugin-react-swc'
import * as path from 'path'

export default defineConfig(({mode}) => {
    const env = loadEnv(mode, process.cwd(), '')
    const appName = env.APP_TYPE || 'cxsun'

    const appRoot = path.resolve(__dirname, `apps/${appName}`)
    const appSrc = path.resolve(appRoot, 'src')

    return {
        root: appRoot,
        plugins: [react()],
        resolve: {
            alias: {
                '@': appSrc,
                "@resources": path.resolve(__dirname, "resources"),
            },
        },
        build: {
            outDir: path.resolve(__dirname, `${appRoot}/dist/`),
            emptyOutDir: true,
        },
        server: {
            port: Number(env.APP_PORT) || 5173,
        },
    }
})
