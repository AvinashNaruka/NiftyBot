# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from signals import generate_signal

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def serve_frontend():
    # if you have index.html in same folder
    try:
        return FileResponse("index.html")
    except:
        return {"msg":"Avinash Trading AI backend running"}

@app.get("/signal")
def signal():
    return generate_signal()
