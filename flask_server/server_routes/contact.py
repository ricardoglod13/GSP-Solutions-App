from flask import request, jsonify
from flask_cors import CORS
from utilities.functions import *
from __init__ import routes

#=============== Contacts ===============#

@routes.route('/contacts', methods=['POST'])
def createContact():
    contact = request.json
    query = f"""INSERT INTO contacto (documento, nombre, telefono, direccion, deuda_contra, tipo) 
            VALUES ("{contact["documento"]}", "{contact["nombre"]}", "{contact["telefono"]}", 
            "{contact["direccion"]}", {contact["deuda_contra"]}, "{contact["tipo"]}");"""
    get_db_connection(query)
    return 'Contacto Creado'

@routes.route('/contacts', methods=['GET'])
def getContact():
    query = f"SELECT * FROM contacto;"
    data = get_db_connection(query, op=True)
    res = json_contact(data)
    return jsonify(res)

@routes.route('/contact/<id>', methods=['GET'])
def getOneContact(id):
    query = f"SELECT * FROM contacto WHERE id = {id};"
    data = get_db_connection(query, op=False)
    res = json_contact(data)
    return jsonify(res)

@routes.route('/contacts/<id>', methods=['DELETE'])
def deleteContact(id):
    query = f"DELETE FROM contacto WHERE id = {id};"
    get_db_connection(query)
    return 'Contacto Eliminado'

@routes.route('/contacts/<id>', methods=['PUT'])
def updateContact(id):
    contact = request.json
    query = f"""UPDATE contacto SET documento = "{contact["documento"]}", nombre = "{contact["nombre"]}", 
            telefono = "{contact["telefono"]}", direccion = "{contact["direccion"]}", 
            deuda_contra = {contact["deuda_contra"]}, deuda_favor = {contact["deuda_favor"]}, 
            tipo = "{contact["tipo"]}" WHERE id = {id};"""
    get_db_connection(query)
    return 'Contacto Actualizado'

