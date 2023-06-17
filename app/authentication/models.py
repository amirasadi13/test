from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "auth_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Token(Base):
    __tablename__= "auth_token"

    id = Column(Integer, primary_key=True, index=True)
    user = relationship("User")
    user_id = Column(ForeignKey("auth_users.id"))
    refresh_token = Column("refresh_token", String, nullable=False)
    expires_at = Column("expires_at", DateTime, nullable=False)
    created_at = Column("created_at", DateTime, server_default=func.now(), nullable=False)
    updated_at = Column("updated_at", DateTime, onupdate=func.now())
