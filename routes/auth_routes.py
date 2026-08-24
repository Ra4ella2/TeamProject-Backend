from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import get_db
from models.user import User
from services.auth_service import AuthService
from middleware.auth_middleware import get_current_user


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

auth_service = AuthService()


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    surname: str
    phone: str = ""


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    result, status_code = auth_service.register(
        db=db,
        email=data.email,
        password=data.password,
        name=data.name,
        surname=data.surname,
        phone=data.phone
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    result, status_code = auth_service.login(
        db=db,
        email=data.email,
        password=data.password
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )


@router.get("/me")
def get_me(
    user: User = Depends(get_current_user)
):
    return {
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "phone": user.phone,
        "balance": user.balance_cents / 100
    }