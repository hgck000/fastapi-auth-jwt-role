from fastapi import FastAPI
from app.api.auth.router import router as auth_router

app = FastAPI(title="FastAPI Auth JWT + Role")

app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "ok"}
