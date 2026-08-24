from sqlalchemy.orm import Session

from models.transaction import Transaction
from models.user import User
from services.transaction_service import TransactionService
from utils.money_utils import amount_to_cents


class WalletService:

    def __init__(self):
        self.transaction_service = TransactionService()

    def get_balance(
        self,
        user: User
    ):
        return {
            "balance": user.balance_cents / 100
        }, 200

    def deposit(
        self,
        db: Session,
        user: User,
        amount
    ):
        amount_cents = amount_to_cents(amount)

        if amount_cents is None:
            return {
                "error": "Сумма должна быть положительной и содержать не более 2 знаков после запятой"
            }, 400

        transaction = Transaction(
            receiver_id=user.id,
            amount_cents=amount_cents,
            type="DEPOSIT",
            status="COMPLETED"
        )

        db.query(User).filter(
            User.id == user.id
        ).update(
            {
                User.balance_cents: User.balance_cents + amount_cents
            },
            synchronize_session=False
        )

        return self.save_operation(
            db,
            user,
            transaction,
            "Баланс успешно пополнен"
        )

    def withdraw(
        self,
        db: Session,
        user: User,
        amount
    ):
        amount_cents = amount_to_cents(amount)

        if amount_cents is None:
            return {
                "error": "Сумма должна быть положительной и содержать не более 2 знаков после запятой"
            }, 400

        transaction = Transaction(
            sender_id=user.id,
            amount_cents=amount_cents,
            type="WITHDRAW",
            status="COMPLETED"
        )

        updated_users = db.query(User).filter(
            User.id == user.id,
            User.balance_cents >= amount_cents
        ).update(
            {
                User.balance_cents: User.balance_cents - amount_cents
            },
            synchronize_session=False
        )

        if not updated_users:
            db.rollback()

            return {
                "error": "Недостаточно средств"
            }, 400

        return self.save_operation(
            db,
            user,
            transaction,
            "Средства успешно выведены"
        )

    def transfer(
        self,
        db: Session,
        user: User,
        receiver_email: str,
        amount
    ):
        amount_cents = amount_to_cents(amount)

        if amount_cents is None:
            return {
                "error": "Сумма должна быть положительной и содержать не более 2 знаков после запятой"
            }, 400

        receiver = db.query(User).filter(
            User.email == receiver_email.strip().lower()
        ).first()

        if not receiver:
            return {
                "error": "Получатель не найден"
            }, 404

        if receiver.id == user.id:
            return {
                "error": "Нельзя перевести деньги самому себе"
            }, 400

        transaction = Transaction(
            sender_id=user.id,
            receiver_id=receiver.id,
            amount_cents=amount_cents,
            type="TRANSFER",
            status="COMPLETED"
        )

        try:
            updated_users = db.query(User).filter(
                User.id == user.id,
                User.balance_cents >= amount_cents
            ).update(
                {
                    User.balance_cents: User.balance_cents - amount_cents
                },
                synchronize_session=False
            )

            if not updated_users:
                db.rollback()

                return {
                    "error": "Недостаточно средств"
                }, 400

            db.query(User).filter(
                User.id == receiver.id
            ).update(
                {
                    User.balance_cents: User.balance_cents + amount_cents
                },
                synchronize_session=False
            )

            db.add(transaction)
            db.commit()
            db.refresh(transaction)
            db.refresh(user)

        except Exception:
            db.rollback()

            return {
                "error": "Не удалось выполнить перевод"
            }, 500

        return {
            "message": "Перевод успешно выполнен",
            "balance": user.balance_cents / 100,
            "transaction": self.transaction_service.serialize_transaction(
                db,
                transaction
            )
        }, 200

    def save_operation(
        self,
        db: Session,
        user: User,
        transaction: Transaction,
        message: str
    ):
        try:
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
            db.refresh(user)

        except Exception:
            db.rollback()

            return {
                "error": "Не удалось выполнить операцию"
            }, 500

        return {
            "message": message,
            "balance": user.balance_cents / 100,
            "transaction": self.transaction_service.serialize_transaction(
                db,
                transaction
            )
        }, 200
