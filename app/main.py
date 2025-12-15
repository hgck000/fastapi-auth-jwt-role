from fastapi import FastAPI
from app.api.auth.router import router as auth_router
from app.api.users.router import router as users_router
from app.api.admin.router import router as admin_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI Auth JWT + Role")
app.include_router(admin_router)

app.include_router(users_router)

app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}
