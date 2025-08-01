// // vite.config.ts
// import {defineConfig, loadEnv} from 'vite'
// import react from '@vitejs/plugin-react-swc'
// import * as path from 'path'
//
// export default defineConfig(({mode}) => {
//     const env = loadEnv(mode, process.cwd(), '')
//     const appName = env.APP_TYPE || 'cxsun'
//
//     const appRoot = path.resolve(__dirname, `apps/${appName}`)
//     const appSrc = path.resolve(appRoot, 'src')
//
//     return {
//         root: appRoot,
//         plugins: [react()],
//         resolve: {
//             alias: {
//                 '@': appSrc,
//                 "@resources": path.resolve(__dirname, "resources"),
//             },
//         },
//         build: {
//             outDir: path.resolve(__dirname, `${appRoot}/dist/`),
//             emptyOutDir: true,
//         },
//         server: {
//             port: Number(env.APP_PORT) || 5173,
//         },
//     }
// })

// vite.config.ts
import {defineConfig, loadEnv} from 'vite'
import react from '@vitejs/plugin-react-swc'
import * as path from 'path'

export default defineConfig(({mode}) => {
        const env = loadEnv(mode, process.cwd(), '')

        const appName = env.APP_TYPE || 'cxsun' // e.g., 'cxsun', 'landing', 'admin'

        const appCategory = env.APP_CATEGORY || 'apps' // 'apps' or 'sites'

        // 🔥 Dynamic root
        const appRoot = path.resolve(__dirname, `${appCategory}/${appName}`)
        const appSrc = path.resolve(appRoot, 'src')

        return {
            root: appRoot,
            plugins: [react()],
            resolve: {
                alias: {
                    '@': appSrc,
                    '@resources': path.resolve(__dirname, 'resources'),
                },
            },
            build: {
                outDir: path.resolve(__dirname, 'public/build'),
                emptyOutDir: true,
                manifest: true,
            },
            server: {
                port: Number(env.APP_PORT) || 3001,
            },
        }
    }
)

want to fix this