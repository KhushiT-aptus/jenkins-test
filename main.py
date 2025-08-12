# main.py
from fastapi import FastAPI

app = FastAPI(title="Demo FastAPI App", version="1.0.0")


@app.get("/")
def root():
    print("root")
    return {"message": "Hello from PIE Applicatn"}
