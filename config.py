import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///wallet.db"
)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "wallet-secret-key-1234567890"
)

JWT_EXPIRATION_HOURS = 24