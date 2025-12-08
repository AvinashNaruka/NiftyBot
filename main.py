from fastapi import FastAPI
from signals import generate_signal

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "Nifty AI Signal Backend Running"}

@app.get("/signal")
def signal():
    return generate_signal()
