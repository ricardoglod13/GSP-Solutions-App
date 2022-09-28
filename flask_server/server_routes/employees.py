from flask import request, jsonify
from utilities.db_queries import db_queries
from __init__ import flask_routes

#=============== Employees ===============#

@flask_routes.route('/employees', methods=['POST'])
def createEmployee():
    employee = request.json
    db_queries('insert', 'empleado',
        documento = f"""{employee["documento"]}""", 
        nombre = f"""{employee["nombre"]}""", 
        telefono = f"""{employee["telefono"]}""", 
        direccion = f"""{employee["direccion"]}""", 
        departamento = f"""{employee["cargo"]}""",
        cargo = f"""{employee["cargo"]}""",
        sueldo = employee["sueldo"],
        tipo_pago = f"""{employee["tipo_pago"]}"""

    )
    return 'Empleado Creado'

@flask_routes.route('/employees', methods=['GET'])
def getEmployees():
    data = db_queries('select', 'empleado', fields=['*'])
    return jsonify(data)

@flask_routes.route('/employee/<id>', methods=['GET'])
def getOneEmployee(id):
    data = db_queries('select', 'empleado', where=['id'], where_value=[id], operators=['='], fields=['*'], fetch=0)
    return jsonify(data)

@flask_routes.route('/employees/<id>', methods=['DELETE'])
def deleteEmployee(id):
    db_queries('delete', 'empleado', where=['id'], where_value=[id], operators=['='])
    return 'Empleado Eliminado'

@flask_routes.route('/employees/<id>', methods=['PUT'])
def updateEmployee(id):
    employee = request.json
    db_queries('update', 'empleado', where=['id'], where_value=[id], operators=['='],
        nombre = f"""{employee["nombre"]}""", 
        telefono = f"""{employee["telefono"]}""", 
        direccion = f"""{employee["direccion"]}""", 
        departamento = f"""{employee["cargo"]}""",
        cargo = f"""{employee["cargo"]}""",
        sueldo = employee["sueldo"],
        tipo_pago = f"""{employee["tipo_pago"]}"""
    )
    return 'Empleado Actualizado'
