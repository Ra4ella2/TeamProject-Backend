from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session

from models.user import User
from utils.jwt_utils import create_token


class AuthService:

    def register(
        self,
        db: Session,
        email: str,
        password: str,
        name: str,
        surname: str,
        phone: str = ""
    ):
        email = email.strip().lower()
        name = name.strip()
        surname = surname.strip()
        phone = phone.strip()

        if not email or not password or not name or not surname:
            return {
                "error": "Заполните обязательные поля"
            }, 400

        if len(password) < 6:
            return {
                "error": "Пароль должен содержать минимум 6 символов"
            }, 400

        existing_user = db.query(User).filter_by(
            email=email
        ).first()

        if existing_user:
            return {
                "error": "Почта уже зарегистрирована"
            }, 400

        password_hash = generate_password_hash(
            password
        )

        user = User(
            name=name,
            surname=surname,
            email=email,
            password_hash=password_hash,
            phone=phone,
            role="USER",
            balance_cents=0
        )

        try:
            db.add(user)
            db.commit()
            db.refresh(user)

        except Exception:
            db.rollback()

            return {
                "error": "Не удалось зарегистрировать пользователя"
            }, 500

        token = create_token(
            user.id
        )

        return {
            "message": "Пользователь успешно зарегистрирован",
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
                "balance": user.balance_cents / 100
            }
        }, 201

    def login(
        self,
        db: Session,
        email: str,
        password: str
    ):
        email = email.strip().lower()

        user = db.query(User).filter_by(
            email=email
        ).first()

        if not user:
            return {
                "error": "Неверная почта или пароль"
            }, 401

        if not check_password_hash(
            user.password_hash,
            password
        ):
            return {
                "error": "Неверная почта или пароль"
            }, 401

        token = create_token(
            user.id
        )

        return {
            "message": "Авторизация успешна",
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
                "balance": user.balance_cents / 100
            }
        }, 200