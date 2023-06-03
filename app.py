from flask import Flask
from flask_cors import CORS,cross_origin
from flask_mysqldb import MySQL



app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={"/*": {"origins": "http://localhost:3000"}})
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'echange_culturel_fsbm'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)