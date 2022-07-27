from time import strftime
from flask import Flask
from flask_cors import CORS
from utilities.init_db import *
from __init__ import routes

app = Flask(__name__)

app.register_blueprint(routes)

#=============== Vaciando Base de Datos ===============#

def empty_database():
    create_db()

if __name__ == '__main__':
    app.run(debug=True)