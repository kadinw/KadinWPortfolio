from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone

from src.housing_predict import lab_app

app = FastAPI()

@app.get("/")
def root():
    raise HTTPException(status_code=404, detail="Not Found")

app.mount("/lab", lab_app)

@app.get("/health")
def health_root():
    return {"time": datetime.now(timezone.utc).isoformat()}

@app.get("/hello")
def hello_root(name: str):
    return {"message": f"Hello {name}"}
