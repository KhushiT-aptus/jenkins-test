# main.py
from fastapi import FastAPI

app = FastAPI(title="Demo FastAPI App", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}
