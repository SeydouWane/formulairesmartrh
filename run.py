from smart_rh import create_app

# Crée l'application Flask
app = create_app()

if __name__ == '__main__':
    # Lance le serveur de développement
    app.run(debug=True)