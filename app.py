from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
# Définir une route pour le login
@app.route('/login', methods=['POST'])
def login():
    # Récupérer les données de login depuis la requête POST
    data = request.get_data()
    data = json.loads(data)
    print(data)
    email = data.get('email')
    password = data.get('password')

    # Vérifier les informations de login
    if email == 'test@example.com' and password == 'password':
        # Si les informations de login sont correctes, renvoyer une réponse JSON avec un message de succès
        response = {'status': 'success', 'message': 'Login réussi !'}
        return (response)
    else:
        # Si les informations de login sont incorrectes, renvoyer une réponse JSON avec un message d'erreur
        response = {'status': 'error', 'message': 'Nom d\'utilisateur ou mot de passe invalide.'}
        return (response)
    


if __name__ == '__main__':
    app.run()