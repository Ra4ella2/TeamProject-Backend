from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from db import init_db

from models.user import User
from models.transaction import Transaction

from routes.auth_routes import router as auth_router
from routes.wallet_routes import router as wallet_router
from routes.transaction_routes import router as transaction_router
from routes.admin_routes import router as admin_router


app = FastAPI(
    title="FinTech Wallet",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


init_db()


app.include_router(
    auth_router
)

app.include_router(
    wallet_router
)

app.include_router(
    transaction_router
)

app.include_router(
    admin_router
)


@app.get("/")
def home():
    return {
        "message": "FinTech Wallet работает"
    }