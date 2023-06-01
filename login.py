from flask import request
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
from app import *


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'echange_culturel_fsbm'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# Route pour le login
@app.route('/Login', methods=['POST'])
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

