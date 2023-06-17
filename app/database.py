from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://user:root@database:5432/postgres'
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()