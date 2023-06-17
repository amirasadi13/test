from __future__ import annotations

from datetime import datetime, timedelta

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .config import auth_config
from ..exceptions import InvalidCredentials
from .models import User, Token
from .schemas import UserCreate, AuthUser
from .utils import get_password_hash, verify_password
from ..utils import generate_random_alphanum

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(db: Session, auth_data: AuthUser) -> User:
    user = get_user_by_email(db, auth_data.email)
    if not user:
        raise InvalidCredentials()

    if not verify_password(auth_data.password, user.hashed_password):
        raise InvalidCredentials()

    return user


def create_refresh_token(db: Session, user_id: int, refresh_token: str = None) -> str:
    if not refresh_token:
        refresh_token = generate_random_alphanum(64)

    expire_refresh_token(db, user_id)
    refresh_token = Token(refresh_token=refresh_token,
                          expires_at=datetime.utcnow() + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
                          user_id=user_id)
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return refresh_token.refresh_token


def get_refresh_token(db: Session, refresh_token: str) -> Token:
    return db.query(Token).filter(Token.refresh_token == refresh_token).first()


def expire_refresh_token(db: Session, user_id: str | int) -> bool:
    db.query(Token).filter(Token.user_id == user_id).delete()
    db.commit()
    return True


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_tokens_list(db: Session):
    return db.query(Token).all()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, email: str):
    return db.query(User).get(User.id == id)


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
