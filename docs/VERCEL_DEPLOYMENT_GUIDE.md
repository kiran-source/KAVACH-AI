# KAVACH AI — Vercel Frontend Deployment Guide

**Target Component**: React 18 + TypeScript + Vite Frontend  
**Platform**: Vercel (Hobby / Pro)  
**Configuration**: Single Page Application (SPA) with Dynamic API Routing  

---

## 1. Vercel Project Import Settings

When importing the KAVACH AI repository into Vercel via GitHub:

| Setting Field | Value | Explanation |
| :--- | :--- | :--- |
| **Framework Preset** | **Vite** | Auto-detected from `frontend/package.json` |
| **Root Directory** | **`frontend`** | Click "Edit" and set to `frontend` so Vercel builds within the client package |
| **Build Command** | `npm run build` | Runs `tsc && vite build` |
| **Output Directory** | `dist` | Generated static bundle output directory |
| **Install Command** | `npm install` | Uses `package-lock.json` |

---

## 2. Environment Variables Configuration

In Vercel Project Settings $\to$ **Environment Variables**:

| Variable Name | Required Value | Purpose |
| :--- | :--- | :--- |
| `VITE_API_URL` | `https://your-backend-host.onrender.com` (or your backend domain) | Base URL for FastAPI backend requests. If left empty, requests fallback to local `/api/v1` proxy. |

> [!SECURITY]
> **Zero Secret Leakage**: Do NOT put `GNANI_API_KEY` into Vercel environment variables! All API keys belong strictly in the backend environment. `VITE_API_URL` is a public endpoint URL only.

---

## 3. SPA Route Rewrite Configuration (`frontend/vercel.json`)

Vite SPAs use client-side routing (`react-router-dom`). Without rewrite configuration, directly refreshing a URL like `https://kavach-ai.vercel.app/incidents` or `/analysis` would cause a Vercel 404.

KAVACH AI includes [frontend/vercel.json](file:///c:/Users/kiran/OneDrive/Documents/Desktop/Kavach/frontend/vercel.json):
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```
This guarantees all frontend sub-routes resolve cleanly to `index.html` on refresh.

---

## 4. Backend CORS Compatibility

The FastAPI backend automatically permits Vercel preview and production domains via regex:
```python
allow_origin_regex=r"https://.*\.vercel\.app"
```
Custom domains can be added to the backend's `ALLOWED_ORIGINS` environment variable (comma-separated).

