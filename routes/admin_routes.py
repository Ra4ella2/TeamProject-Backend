from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db import get_db
from middleware.auth_middleware import get_current_admin
from models.user import User
from services.admin_service import AdminService


router = APIRouter(
    prefix="/api/admin",
    tags=["admin"]
)

admin_service = AdminService()


@router.get("/users")
def get_users(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result, status_code = admin_service.get_users(
        db
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )


@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result, status_code = admin_service.get_user(
        db,
        user_id
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )


@router.get("/transactions")
def get_transactions(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result, status_code = admin_service.get_transactions(
        db
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )


@router.get("/stats")
def get_stats(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result, status_code = admin_service.get_stats(
        db
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )