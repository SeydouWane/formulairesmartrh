import os

class Config:
    # Clé secrète pour sécuriser les sessions et formulaires
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre-cle-secrete-par-defaut-tres-securisee'
    
    # Configuration de la base de données PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:aipenpass123@localhost:5432/smart_rh_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False