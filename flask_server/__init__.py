from flask import Blueprint
flask_routes = Blueprint('flask_routes', __name__)

from server_routes import product, contact, employees, transaction, payment, excel_templates
