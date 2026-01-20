from app.database import engine, Base
from app import models  # IMPORT OBBLIGATORIO

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ Database inizializzato")
