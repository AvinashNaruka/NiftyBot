from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from signals import generate_signal

app = FastAPI()

# -----------------------------
# CORS FIX (MOST IMPORTANT PART)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
app.mount("/static", StaticFiles(directory="."), name="static")


# Home → return HTML
@app.get("/")
def frontend():
    return FileResponse("index.html")


# Backend API route
@app.get("/signal")
def signal_api():
    try:
        result = generate_signal()
        return result
    except Exception as e:
        return {"error": "internal", "message": str(e)}
