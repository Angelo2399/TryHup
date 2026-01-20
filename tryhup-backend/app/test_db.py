from database import engine

try:
    connection = engine.connect()
    print("✅ Connessione al database riuscita!")
    connection.close()
except Exception as e:
    print("❌ Errore di connessione:")
    print(e)
