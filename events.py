from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from app import *


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'echange_culturel_fsbm'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Route pour récupérer tous les événements
@app.route('/events', methods=['GET'])
def get_events():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events")
    events = cur.fetchall()
    cur.close()
    return jsonify(events)

# Route pour ajouter un nouvel événement
@app.route('/events/add', methods=['POST'])
def add_event():
    title = request.json['title']
    description = request.json['description']
    date = request.json['date']
    location = request.json['location']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO events (title, description, date, location) VALUES (%s, %s, %s, %s)",
                (title, description, date, location))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Événement ajouté avec succès'})

# Route pour confirmer un événement
@app.route('/events/confirm/<int:event_id>', methods=['POST'])
def confirm_event(event_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE events SET isConfirmed = 1 WHERE id = %s", (event_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Confirmation réussie'})

# Route pour filtrer les événements par date
@app.route('/events/filter', methods=['POST'])
def filter_events():
    start_date = request.json['start_date']
    end_date = request.json['end_date']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events WHERE date BETWEEN %s AND %s", (start_date, end_date))
    filtered_events = cur.fetchall()
    cur.close()

    return jsonify(filtered_events)

# Route pour supprimer un événement
@app.route('/events/delete/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM events WHERE id = %s", (event_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Événement supprimé avec succès'})

# Route pour modifier un événement
@app.route('/events/edit/<int:event_id>', methods=['PUT'])
def edit_event(event_id):
    title = request.json['title']
    description = request.json['description']
    date = request.json['date']
    location = request.json['location']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE events SET title = %s, description = %s, date = %s, location = %s WHERE id = %s",
                (title, description, date, location, event_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Événement modifié avec succès'})

