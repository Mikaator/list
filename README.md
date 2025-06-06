# Einkaufslisten App

Eine moderne Webanwendung zum Erstellen und Verwalten von Einkaufslisten in Gruppen.

## Features

- Gruppenbasierte Authentifizierung
- Erstellen und Verwalten von Einkaufslisten
- Hinzufügen und Bearbeiten von Artikeln
- Anpassbare Icons für Artikel
- Modernes Dark Mode Design
- Responsive Benutzeroberfläche

## Installation

1. Klonen Sie das Repository:
```bash
git clone <repository-url>
cd einkaufslisten-app
```

2. Erstellen Sie eine virtuelle Umgebung und aktivieren Sie sie:
```bash
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate
```

3. Installieren Sie die Abhängigkeiten:
```bash
pip install -r requirements.txt
```

4. Setzen Sie die Umgebungsvariablen:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY=your-secret-key
```

5. Initialisieren Sie die Datenbank:
```bash
flask db init
flask db migrate
flask db upgrade
```

6. Starten Sie die Anwendung:
```bash
flask run
```

## Deployment auf Render.com

1. Erstellen Sie ein neues Repository auf GitHub und pushen Sie den Code.

2. Gehen Sie zu [Render.com](https://render.com) und erstellen Sie ein neues Web Service.

3. Verbinden Sie Ihr GitHub-Repository.

4. Konfigurieren Sie das Deployment:
   - Name: einkaufslisten-app (oder ein Name Ihrer Wahl)
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

5. Fügen Sie die folgenden Umgebungsvariablen hinzu:
   - `SECRET_KEY`: Ein sicherer Schlüssel für die Anwendung
   - `DATABASE_URL`: Die URL Ihrer Datenbank (wird von Render.com bereitgestellt)

6. Klicken Sie auf "Create Web Service"

## Technologien

- Backend: Python/Flask
- Frontend: HTML, CSS (Tailwind CSS), JavaScript
- Datenbank: SQLite (Entwicklung) / PostgreSQL (Produktion)
- Deployment: Render.com
- Icons: Font Awesome 