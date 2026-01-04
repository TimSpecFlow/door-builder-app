# Door Builder Frontend

Small React single-page app (Vite) that calls the Django backend `/api/estimate/` endpoint and shows live price estimates.

Quick start (PowerShell):

```powershell
cd "c:\Users\obrie\Python\door-builder-app\frontend"
npm install
npm run dev
```

The dev server proxies `/api` to the local Django server (configured in `vite.config.js`).
