from typing import Annotated
from fastapi import Depends

from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from .config import auth_config
from ..exceptions import RefreshTokenNotValid, InvalidToken
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/login", auto_error=False)


def create_access_token(*, user: User, expires_delta: timedelta = timedelta(minutes=auth_config.JWT_EXP), ) -> str:
    jwt_data = {
        "sub": str(user.id),
        "exp": datetime.utcnow() + expires_delta
    }

    return jwt.encode(jwt_data, auth_config.JWT_SECRET, algorithm=auth_config.JWT_ALG)


def valid_token(*, token: Annotated[str, Depends(oauth2_scheme)]):
    if not token:
        InvalidToken()
    try:
        payload = jwt.decode(
            token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG]
        )
        if _validate_token_expire_date(float(payload['exp'])):
            return payload
        raise RefreshTokenNotValid()
    except JWTError:
        raise InvalidToken()


def _validate_token_expire_date(token_expire_time: float) -> bool:
    return token_expire_time > datetime.utcnow().timestamp()

