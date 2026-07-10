import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import "../../../design-tokens/generated/nimble.tokens.css";
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
