# smart_rh/run.py ou fichier principal de lancement

from smart_rh import create_app

app = create_app()

# Modifiez la ligne d'exécution de Flask pour inclure host='0.0.0.0'
if __name__ == '__main__':
    # RENDER utilise généralement le port 10000, 8080 ou 5000, mais il doit BIND à 0.0.0.0
    app.run(host='0.0.0.0', port=5000, debug=True) 
    # Assurez-vous que RENDER_EXTERNAL_HOSTNAME est configuré si vous avez besoin d'un hôte spécifique.
