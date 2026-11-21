from fastapi import FastAPI

app = FastAPI(title="COSMOS API")

@app.get("/")
def home():
    return {
        "message": "Welcome to COSMOS API"
    }