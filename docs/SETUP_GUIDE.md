# KAVACH AI — Installation, Setup & Execution Guide

**Target Environment**: Windows 10/11, macOS, Linux  
**Runtime Requirements**: Python 3.10+, Node.js 18+, npm 9+

---

## 1. Prerequisites Installation

1. **Python Environment**:
   - Ensure Python 3.10 or higher is installed:
     ```bash
     python --version
     ```
2. **Node.js Environment**:
   - Ensure Node.js and npm are installed:
     ```bash
     node --version
     npm --version
     ```

---

## 2. Environment Configuration

Copy the example environment configuration into `backend/.env`:
```powershell
cp backend/.env.example backend/.env
```

Ensure the following variables are defined in `backend/.env`:
```env
# Gnani AI API Credentials
GNANI_API_KEY="YOUR_ACTUAL_API_KEY"
GNANI_PRISMA_ENDPOINT="https://api.vachana.ai/stt/v3"
GNANI_TIMBRE_ENDPOINT="https://api.vachana.ai/api/v1/tts/inference"

# Application Settings
DEMO_MODE=false
DATABASE_URL="sqlite:///./kavach.db"
UPLOAD_DIR="./uploads"
```
*Note: If `GNANI_API_KEY` is not provided or set to a placeholder, KAVACH AI automatically operates in labeled Demo Mode with local simulation fallbacks, ensuring evaluators can test without active credentials.*

---

## 3. Backend Setup & Execution

```powershell
# 1. Navigate to backend directory
cd backend

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Verify test suite (all 78 tests should pass)
pytest tests/ -v

# 4. Start the FastAPI development server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
The backend API is now live at `http://127.0.0.1:8000`. Interactive OpenAPI documentation is accessible at `http://127.0.0.1:8000/docs`.

---

## 4. Frontend Setup & Execution

In a second terminal window:
```powershell
# 1. Navigate to frontend directory
cd frontend

# 2. Install frontend dependencies
npm install

# 3. Run production build check
npm run build

# 4. Start Vite development server
npm run dev
```
The frontend interface will launch at `http://localhost:5173`.

---

## 5. Live Smoke Test Commands

To verify that the application and the hybrid threat interception engine are fully responsive, execute the following PowerShell command:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/hybrid/analyze" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text": "I am calling from CBI headquarters. You are placed under digital arrest.", "language": "en"}'
```
Expected response:
```json
{
  "status": "SUCCESS",
  "final_decision": "SCAM",
  "final_risk_score": 85.0,
  "severity": "Critical",
  "critical_rule_triggered": true,
  "rule_shield_active": true
}
```

