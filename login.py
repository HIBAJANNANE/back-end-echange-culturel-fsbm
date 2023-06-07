from flask import request,jsonify
from flask import session
import bcrypt
from app import *




# Route pour le login
@app.route('/login', methods=['POST'])
def login():
    # Récupérer les données de login depuis la requête POST
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s and password= %s", (email,password,))
    user = cur.fetchone()
    cur.close()

    if user:
        # Comparer le mot de passe fourni avec le mot de passe haché stocké dans la base de données
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Si les informations de login sont correctes, renvoyer une réponse JSON avec un message de succès
            response = {'status': 'success', 'message': 'Login réussi !'}
            return response

    # Si les informations de login sont incorrectes ou l'utilisateur n'existe pas, renvoyer une réponse JSON avec un message d'erreur
    response = {'status': 'error', 'message': 'Nom d\'utilisateur ou mot de passe invalide.'}
    return response

@app.route('/logout')
def logout():
    session.clear()

# Route pour le sign up
@app.route('/signUp', methods=['POST'])
def signup():
    # Récupérer les données d'inscription depuis la requête POST
    data = request.get_json()
    nom = data.get('nom')
    prenom = data.get('prenom')
    role = data.get('role')
    email = data.get('email')
    password = data.get('password')
   

    # Vérifier si l'utilisateur existe déjà dans la base de données
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s and password= %s", (email,password,))
    existing_user = cur.fetchone()
    
    if existing_user:
        cur.close()
        response = {'status': 'error', 'message': 'Cet utilisateur existe déjà.'}
        return jsonify(response)

    # Hacher le mot de passe avant de le stocker dans la base de données
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insérer les informations de l'utilisateur dans la base de données
    cur.execute("INSERT INTO users (nom, prenom,role, email, password) VALUES (%s, %s,%s, %s, %s)",
                (nom, prenom,role, email, hashed_password))
    mysql.connection.commit()
    cur.close()

    # Renvoyer une réponse JSON avec un message de succès
    response = {'status': 'success', 'message': 'Inscription réussie !'}
    return jsonify(response)

