from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def root():
    raise HTTPException(status_code=404, detail="Not Found")

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/hello")
def hello(name: str):
    return {"message": f"Hello {name}"}
