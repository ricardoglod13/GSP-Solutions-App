from flask import request, jsonify
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
    data = db_queries('select', 'producto', fields=['*'])
    return jsonify(data)

@flask_routes.route('/product/<id>', methods=['GET'])
def getOneProduct(id):
    data = db_queries('select', 'producto', where=['id'], where_value=[id], operators=['='], fields=['*'], fetch=0)
    return jsonify(data)

@flask_routes.route('/products/<id>', methods=['DELETE'])
def deleteProduct(id):
    db_queries('delete', 'producto', where=['id'], where_value=[id], operators=['='])
    return 'Producto Eliminado'

@flask_routes.route('/products/<id>', methods=['PUT'])
def updateProduct(id):
    product = request.json
    db_queries('update', 'producto', where=['id'], where_value=[id], operators=['='],
        codigo = f"""{product["codigo"]}""",
        tipo = f"""{product["tipo"]}""",
        descripcion = f"""{product["descripcion"]}""",
        precio_costo = product["precio_costo"],
        precio_venta = product["precio_venta"],
        cantidad = product["cantidad"]
    )
    return 'Producto Actualizado'
