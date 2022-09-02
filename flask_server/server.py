from time import strftime
from flask import Flask
from flask_cors import CORS
from utilities.init_db import *
from __init__ import flask_routes

app = Flask(__name__)

app.register_blueprint(flask_routes)

CORS(app)

#=============== Vaciando Base de Datos ===============#

def empty_database():
    create_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')