import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

const app_type = import.meta.env.APP_TYPE || 'cms'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App app_type={app_type} />
  </StrictMode>,
)
