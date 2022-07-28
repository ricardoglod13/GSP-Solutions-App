from flask import request, jsonify
from flask_cors import CORS
from utilities.functions import json_product
from utilities.db_queries import db_queries
from __init__ import flask_routes

#=============== Products ===============#

@flask_routes.route('/products', methods=['POST'])
def createProduct():
    product = request.json
    db_queries('insert', 'producto', 
        codigo = f"""{product["codigo"]}""", 
        tipo = f"""{product["tipo"]}""",
        descripcion = f"""{product["descripcion"]}""",
        precio_costo = product["precio_costo"],
        precio_venta = product["precio_venta"],
        cantidad = product["cantidad"]
    )
    return 'Producto Creado'

@flask_routes.route('/products', methods=['GET'])
def getProduct():
    data = db_queries('select', 'producto')
    res = json_product(data)
    return jsonify(res)

@flask_routes.route('/product/<id>', methods=['GET'])
def getOneProduct(id):
    data = db_queries('select', 'producto', where='id', where_value=id)
    res = json_product(data)
    return jsonify(res)

@flask_routes.route('/products/<id>', methods=['DELETE'])
def deleteProduct(id):
    db_queries('delete', 'producto', where='id', where_value=id)
    return 'Producto Eliminado'

@flask_routes.route('/products/<id>', methods=['PUT'])
def updateProduct(id):
    product = request.json
    db_queries('update', 'producto', where='id', where_value=id,
        codigo = f"""{product["codigo"]}""",
        tipo = f"""{product["tipo"]}""",
        descripcion = f"""{product["descripcion"]}""",
        precio_costo = product["precio_costo"],
        precio_venta = product["precio_venta"],
        cantidad = product["cantidad"]
    )
    return 'Producto Actualizado'
