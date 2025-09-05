import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

function App() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold">Hello Qlick</h1>
      <p className="text-muted-foreground mt-2">QR menü + sipariş + AI upsell</p>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)


