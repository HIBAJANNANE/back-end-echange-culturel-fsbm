from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

users = []  # Liste des utilisateurs enregistrés

# Route pour le login
@app.route('/login', methods=['POST'])
def login():
    # Récupérer les données de login depuis la requête POST
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Vérifier les informations de login
    for user in users:
        if user['email'] == email and user['password'] == password:
            # Si les informations de login sont correctes, renvoyer une réponse JSON avec un message de succès
            response = {'status': 'success', 'message': 'Login réussi !'}
            return (response)

    # Si les informations de login sont incorrectes, renvoyer une réponse JSON avec un message d'erreur
    response = {'status': 'error', 'message': 'Nom d\'utilisateur ou mot de passe invalide.'}
    return (response)

# Route pour le sign up
@app.route('/signup', methods=['POST'])
def signup():
    # Récupérer les données d'inscription depuis la requête POST
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    # Vérifier si l'utilisateur existe déjà
    for user in users:
        if user['email'] == email:
            response = {'status': 'error', 'message': 'Cet utilisateur existe déjà.'}
            return (response)

    # Ajouter l'utilisateur à la liste des utilisateurs enregistrés
    user = {'email': email, 'password': password, 'first_name': first_name, 'last_name': last_name}
    users.append(user)

    # Renvoyer une réponse JSON avec un message de succès
    response = {'status': 'success', 'message': 'Inscription réussie !'}
    return (response)


if __name__ == '__main__':
    app.run()
