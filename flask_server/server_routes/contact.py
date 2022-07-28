from flask import request, jsonify
from utilities.functions import json_contact
from utilities.db_queries import db_queries
from __init__ import flask_routes

#=============== Contacts ===============#

@flask_routes.route('/contacts', methods=['POST'])
def createContact():
    contact = request.json
    db_queries('insert', 'contacto',
        documento = f"""{contact["documento"]}""", 
        nombre = f"""{contact["nombre"]}""", 
        telefono = f"""{contact["telefono"]}""", 
        direccion = f"""{contact["direccion"]}""", 
        deuda_contra = contact["deuda_contra"],
        deuda_favor = contact["deuda_favor"],
        tipo = f"""{contact["tipo"]}"""
    )
    return 'Contacto Creado'

@flask_routes.route('/contacts', methods=['GET'])
def getContact():
    data = db_queries('select', 'contacto')
    res = json_contact(data)
    return jsonify(res)

@flask_routes.route('/contact/<id>', methods=['GET'])
def getOneContact(id):
    data = db_queries('select', 'contacto', where='id', where_value=id)
    res = json_contact(data)
    return jsonify(res)

@flask_routes.route('/contacts/<id>', methods=['DELETE'])
def deleteContact(id):
    db_queries('delete', 'contacto', where='id', where_value=id)
    return 'Contacto Eliminado'

@flask_routes.route('/contacts/<id>', methods=['PUT'])
def updateContact(id):
    contact = request.json
    db_queries('update', 'contacto', where='id', where_value=id,
        nombre = f"""{contact["nombre"]}""", 
        telefono = f"""{contact["telefono"]}""", 
        direccion = f"""{contact["direccion"]}""", 
        tipo = f"""{contact["tipo"]}"""
    )
    return 'Contacto Actualizado'

