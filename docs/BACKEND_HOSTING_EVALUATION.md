# KAVACH AI — Backend Hosting Architecture & Feasibility Evaluation

**Component**: FastAPI Python Backend & ML Inference Engine  
**Hardware Profile**: ~1.2 GB RAM (with MuRIL loaded), Multi-Core CPU  

---

## 1. Hosting Feasibility Matrix

| Hosting Platform | Free Tier Feasibility | RAM Capacity | Max Bundle Size | Verdict for KAVACH AI |
| :--- | :---: | :---: | :---: | :--- |
| **Vercel Serverless Functions** | Infeasible | Max 1024 MB | 250 MB max | **INCOMPATIBLE**: MuRIL weights (950 MB) + PyTorch CPU (~180 MB) exceed Vercel's 250 MB serverless artifact limit. |
| **Render Web Service** | Partial (Baseline only) | 512 MB (Free) | No strict limit | **RESTRICTED**: Can run Production Baseline v1 and TF-IDF v3. Will OOM if full MuRIL v1 weights (950 MB) are loaded into 512 MB RAM. |
| **Railway / Fly.io** | Feasible with trial credit | 1 GB – 2 GB | Container-based | **FEASIBLE**: Supports full MuRIL inference if allocated $\ge 1.5$ GB RAM. |
| **Cloudflare Tunnel to Local Host (Recommended for Hackathon Demo)** | **100% FREE & FULLY CAPABLE** | Full Host RAM (16 GB) | Unlimited | **RECOMMENDED**: Exposes your live local FastAPI server (which already has MuRIL and PyTorch loaded) to a public HTTPS URL with zero hosting cost and full performance. |

---

## 2. Recommended Deployment Architecture: Hybrid Production Setup

```
[Vercel Public Frontend] (https://kavach-ai.vercel.app)
         │
         │ HTTPS API Requests (VITE_API_URL)
         ▼
[Public HTTPS Gateway]
  - Option A: Cloudflare Tunnel to Local Server (Zero cost, full 16GB RAM & MuRIL support)
  - Option B: Render / Railway Container (Production baseline or scaled container)
         │
         ▼
[FastAPI Backend Server] (Python 3.13 / Uvicorn)
  - Stage 0: Rule-Priority Shield
  - Stage 1: TF-IDF v3 Fast Path (4.29 ms)
  - Stage 2: MuRIL v1 Selective Escalation
```

---

## 3. Step-by-Step Instructions: Zero-Cost Cloudflare Tunnel Setup

To connect your Vercel frontend to your live KAVACH backend in 60 seconds without paying for cloud servers:

1. **Start the Local Backend**:
   ```powershell
   cd backend
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```
2. **Start Cloudflare Tunnel** (Requires free `cloudflared` CLI or `npx cloudflared`):
   ```powershell
   npx cloudflared tunnel --url http://127.0.0.1:8000
   ```
3. **Capture Public HTTPS URL**:
   Cloudflare outputs a public URL: `https://xxxx.trycloudflare.com`.
4. **Set Vercel Environment Variable**:
   In Vercel Dashboard $\to$ Settings $\to$ Environment Variables:
   - `VITE_API_URL` = `https://xxxx.trycloudflare.com`
5. **Redeploy Vercel**:
   Your frontend is now live with full speech recognition, MuRIL deep learning, and zero hosting fees!

---

## 4. Backend Environment Variable Checklist

When configuring any host environment (local or cloud):

| Variable Name | Production Value Example | Required? |
| :--- | :--- | :---: |
| `GNANI_API_KEY` | `YOUR_ACTUAL_API_KEY` | Yes (for live Prisma/Timbre) |
| `GNANI_PRISMA_ENDPOINT` | `https://api.vachana.ai/stt/v3` | Yes |
| `GNANI_TIMBRE_ENDPOINT` | `https://api.vachana.ai/api/v1/tts/inference` | Yes |
| `DEMO_MODE` | `false` | Yes |
| `ALLOWED_ORIGINS` | `https://kavach-ai.vercel.app,http://localhost:5173` | Yes |
| `DATABASE_URL` | `sqlite:///./kavach.db` | Yes |
| `UPLOAD_DIR` | `./uploads` | Yes |
| `MAX_UPLOAD_SIZE_MB` | `25` | Yes |
