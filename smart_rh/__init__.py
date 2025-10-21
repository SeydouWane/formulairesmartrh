from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Charger les variables d'environnement (DB_URL, SECRET_KEY, etc.)
load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('smart_rh.config.Config')

    # Initialiser les extensions
    db.init_app(app)

    # Enregistrer les routes (Blueprint)
    from smart_rh.routes import main
    app.register_blueprint(main)

    # Initialisation de la base de données
    with app.app_context():
        db.create_all() # Crée les tables si elles n'existent pas
        
    return app