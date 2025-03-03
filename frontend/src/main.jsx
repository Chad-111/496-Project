import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Signup from './Signup.jsx'
import Login from './Login.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

/* DO NOT RUN THIS ON EXPOSED SERVER
this contains raw SQL input, need to implement protections.
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Login />
    <Signup />
  </StrictMode>,
) */
