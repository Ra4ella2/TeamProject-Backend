from sqlalchemy import func
from sqlalchemy.orm import Session

from models.transaction import Transaction
from models.user import User
from services.transaction_service import TransactionService


class AdminService:

    def __init__(self):
        self.transaction_service = TransactionService()

    def get_users(
        self,
        db: Session
    ):
        users = db.query(User).order_by(
            User.id.asc()
        ).all()

        return {
            "users": [
                self.serialize_user(user)
                for user in users
            ]
        }, 200

    def get_user(
        self,
        db: Session,
        user_id: int
    ):
        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:
            return {
                "error": "Пользователь не найден"
            }, 404

        return self.serialize_user(
            user
        ), 200

    def get_transactions(
        self,
        db: Session
    ):
        transactions = db.query(
            Transaction
        ).order_by(
            Transaction.created_at.desc()
        ).all()

        return {
            "transactions": [
                self.transaction_service.serialize_transaction(
                    db,
                    transaction
                )
                for transaction in transactions
            ]
        }, 200

    def get_stats(
        self,
        db: Session
    ):
        users_count = db.query(
            func.count(User.id)
        ).scalar()

        transactions_count = db.query(
            func.count(Transaction.id)
        ).scalar()

        total_balance_cents = db.query(
            func.coalesce(
                func.sum(User.balance_cents),
                0
            )
        ).scalar()

        return {
            "users_count": users_count,
            "transactions_count": transactions_count,
            "total_balance": total_balance_cents / 100
        }, 200

    def serialize_user(
        self,
        user: User
    ):
        return {
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "balance": user.balance_cents / 100,
            "createdAt": user.created_at.isoformat()
        }