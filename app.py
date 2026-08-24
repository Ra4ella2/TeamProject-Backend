from fastapi import FastAPI

from db import init_db
from models.user import User
from models.transaction import Transaction

from routes.auth_routes import router as auth_router
from routes.wallet_routes import router as wallet_router
from routes.transaction_routes import router as transaction_router


app = FastAPI(
    title="FinTech Wallet",
    version="1.0.0"
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


@app.get("/")
def home():
    return {
        "message": "FinTech Wallet работает"
    }
