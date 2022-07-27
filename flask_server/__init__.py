from flask import Blueprint
routes = Blueprint('routes', __name__)

from server_routes import product, contact, sale, payment
