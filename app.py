from fastapi import FastAPI

from db import init_db
from models.user import User

from routes.auth_routes import router as auth_router


app = FastAPI(
    title="FinTech Wallet",
    version="1.0.0"
)


init_db()


app.include_router(
    auth_router
)


@app.get("/")
def home():
    return {
        "message": "FinTech Wallet работает!"
    }