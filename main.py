from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from signals import generate_signal

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"]
)

@app.get("/signal")
def signal(request: Request):
    manual_ltp = request.query_params.get("ltp")
    return generate_signal(manual_ltp)
