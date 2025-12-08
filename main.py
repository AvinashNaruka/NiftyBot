from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from signals import generate_signal

app = FastAPI()

# Serve frontend files
app.mount("/static", StaticFiles(directory="."), name="static")

# Home → Frontend page
@app.get("/")
def frontend():
    return FileResponse("index.html")


# API route
@app.get("/signal")
def signal():
    return generate_signal()
