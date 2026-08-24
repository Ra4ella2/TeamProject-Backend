from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db import get_db
from middleware.auth_middleware import get_current_user
from models.user import User
from services.transaction_service import TransactionService


router = APIRouter(
    prefix="/api/transactions",
    tags=["transactions"]
)

transaction_service = TransactionService()


@router.get("")
def get_history(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result, status_code = transaction_service.get_history(
        db,
        user
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )


@router.get("/{transaction_id}")
def get_details(
    transaction_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result, status_code = transaction_service.get_details(
        db,
        user,
        transaction_id
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )
