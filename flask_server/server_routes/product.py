from flask import request, jsonify
from flask_cors import CORS
from utilities.functions import *
from __init__ import routes

#=============== Products ===============#

@routes.route('/products', methods=['POST'])
def createProduct():
    product = request.json
    query = f"""INSERT INTO producto (codigo, tipo, descripcion, precio_costo, precio_venta, cantidad) 
            VALUES ("{product["codigo"]}", "{product["tipo"]}", "{product["descripcion"]}", {product["precio_costo"]}, 
            {product["precio_venta"]}, {product["cantidad"]});"""
    get_db_connection(query)
    return 'Producto Creado'

@routes.route('/products', methods=['GET'])
def getProduct():
    query = f"SELECT * FROM producto;"
    data = get_db_connection(query, op=True)
    res = json_product(data)
    return jsonify(res)

@routes.route('/product/<id>', methods=['GET'])
def getOneProduct(id):
    query = f"SELECT * FROM producto WHERE id = {id};"
    data = get_db_connection(query, op=False)
    res = json_product(data)
    return jsonify(res)

@routes.route('/products/<id>', methods=['DELETE'])
def deleteProduct(id):
    query = f"DELETE FROM producto WHERE id = {id};"
    get_db_connection(query)
    return 'Producto Eliminado'

@routes.route('/products/<id>', methods=['PUT'])
def updateProduct(id):
    product = request.json
    query = f"""UPDATE producto SET codigo = "{product["codigo"]}", descripcion = "{product["descripcion"]}", 
            precio_costo = {product["precio_costo"]}, precio_venta = {product["precio_venta"]}, 
            cantidad = {product["cantidad"]} WHERE id = {id};"""
    get_db_connection(query)
    return 'Producto Actualizado'
