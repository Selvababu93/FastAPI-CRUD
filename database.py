from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends
from typing import Annotated


# DATABASE_URL = "sqlite:///./today_practice.db"
DATABASE_URL = "postgresql://postgres:Asdf321$@localhost/TodoApplicationDatabase"

engine = create_engine(url=DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
db_dependency = Annotated[Session, Depends(get_db)]