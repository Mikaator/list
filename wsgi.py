from app import app, init_db

# Initialisiere die Datenbank beim Start
init_db()

if __name__ == "__main__":
    app.run() 