from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class AccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class AuthUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class Token(BaseModel):
    user_id: int = Field(alias="user_id")

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
