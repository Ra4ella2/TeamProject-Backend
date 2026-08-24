from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.transaction import Transaction
from models.user import User


class TransactionService:

    def get_history(
        self,
        db: Session,
        user: User
    ):
        transactions = db.query(Transaction).filter(
            or_(
                Transaction.sender_id == user.id,
                Transaction.receiver_id == user.id
            )
        ).order_by(
            Transaction.created_at.desc()
        ).all()

        return {
            "transactions": [
                self.serialize_transaction(db, transaction)
                for transaction in transactions
            ]
        }, 200

    def get_details(
        self,
        db: Session,
        user: User,
        transaction_id: int
    ):
        transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id
        ).first()

        if not transaction:
            return {
                "error": "Транзакция не найдена"
            }, 404

        if user.id not in (
            transaction.sender_id,
            transaction.receiver_id
        ):
            return {
                "error": "Нет доступа к этой транзакции"
            }, 403

        return self.serialize_transaction(db, transaction), 200

    def serialize_transaction(
        self,
        db: Session,
        transaction: Transaction
    ):
        sender = self.get_user_data(
            db,
            transaction.sender_id
        )
        receiver = self.get_user_data(
            db,
            transaction.receiver_id
        )

        return {
            "id": transaction.id,
            "sender": sender,
            "receiver": receiver,
            "amount": transaction.amount_cents / 100,
            "type": transaction.type,
            "status": transaction.status,
            "createdAt": transaction.created_at.isoformat()
        }

    def get_user_data(
        self,
        db: Session,
        user_id: int | None
    ):
        if user_id is None:
            return None

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:
            return None

        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "surname": user.surname
        }
