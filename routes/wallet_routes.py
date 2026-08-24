from decimal import Decimal

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import get_db
from middleware.auth_middleware import get_current_user
from models.user import User
from services.wallet_service import WalletService


router = APIRouter(
    prefix="/api/wallet",
    tags=["wallet"]
)

wallet_service = WalletService()


class AmountRequest(BaseModel):
    amount: Decimal


class TransferRequest(AmountRequest):
    receiver_email: str


@router.get("/balance")
def get_balance(
    user: User = Depends(get_current_user)
):
    result, status_code = wallet_service.get_balance(user)

    return JSONResponse(
        status_code=status_code,
        content=result
    )


@router.post("/deposit")
def deposit(
    data: AmountRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result, status_code = wallet_service.deposit(
        db,
        user,
        data.amount
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )


@router.post("/withdraw")
def withdraw(
    data: AmountRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result, status_code = wallet_service.withdraw(
        db,
        user,
        data.amount
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )


@router.post("/transfer")
def transfer(
    data: TransferRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result, status_code = wallet_service.transfer(
        db,
        user,
        data.receiver_email,
        data.amount
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )
