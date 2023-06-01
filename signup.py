from app import app
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import bcrypt

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'echange_culturel_fsbm'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# Route pour le sign up
@app.route('/signUp', methods=['POST'])
def signup():
    # Récupérer les données d'inscription depuis la requête POST
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    nom = data.get('nom')
    prenom = data.get('prenom')

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
    cur.execute("INSERT INTO users (nom, prenom, email, password) VALUES (%s, %s, %s, %s)",
                (nom, prenom, email, hashed_password))
    mysql.connection.commit()
    cur.close()

    # Renvoyer une réponse JSON avec un message de succès
    response = {'status': 'success', 'message': 'Inscription réussie !'}
    return jsonify(response)
