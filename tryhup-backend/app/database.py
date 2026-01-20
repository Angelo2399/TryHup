from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# print("DEBUG DATABASE_URL =", DATABASE_URL)  # ⛔ togli in produzione

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


# ✅ UNICA funzione get_db (centralizzata)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
