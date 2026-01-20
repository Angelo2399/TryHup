from app.database import engine, Base
import app.models  # carica i modelli


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("✅ Database inizializzato")
