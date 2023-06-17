from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from .services import get_user_by_email, create_user as register_user, authenticate_user, \
    create_refresh_token, get_tokens_list
from .dependencies import create_access_token
from .schemas import UserCreate, AccessTokenResponse, AuthUser
from ..database import get_database

router = APIRouter()


@router.post("/users/register/", response_model=AccessTokenResponse)
def register(user: UserCreate, db: Session = Depends(get_database)) -> AccessTokenResponse:
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = register_user(db=db, user=user)
    refresh_token_value = create_refresh_token(db=db, user_id=user.id)
    return AccessTokenResponse(
        access_token=create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.post("/users/login/", response_model=AccessTokenResponse)
def login(auth_data: AuthUser, db: Session = Depends(get_database)) -> AccessTokenResponse:
    user = authenticate_user(db, auth_data)
    refresh_token_value = create_refresh_token(db=db, user_id=user.id)
    return AccessTokenResponse(
        access_token=create_access_token(user=user),
        refresh_token=refresh_token_value,
    )

