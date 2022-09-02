from flask import request, jsonify
from utilities.functions import *
from utilities.db_queries import db_queries
from __init__ import flask_routes
import datetime

#=============== Transactions ===============#

@flask_routes.route('/transactions', methods=['POST'])
def createTransaction():
    transaction = request.json
    date = datetime.datetime.now()
    db_queries('insert', 'transaccion',
        acreedor = f"""{transaction["acreedor"]}""", 
        deudor = f"""{transaction["deudor"]}""",
        items = f"""[]""", 
        plazo = transaction["plazo"],
        cantidad_pagada = 0,
        total = 0.0,
        tipo = transaction['tipo'],
        fecha = f"""{date.strftime("%Y/%m/%d")}"""
    )
    return 'Transaccion creada'

@flask_routes.route('/transactions/<code>/<cant>/<id_transaction>', methods=['POST'])
def addItems(code, cant, id_transaction):
    new_data_transaction = []
    aux = 0

    #============== Seleccionando el producto ===============#
    res_product = db_queries('select', 'producto', where=['codigo'], where_value=[code], operators=['='], fields=['*'], fetch=0)
    res_product['cantidad'] = int(cant)
    res_product['subtotal'] = int(cant) * res_product['precio_venta']

    #=============== Verificando si la venta ya tiene items agregados ===============#
    data_transaction = db_queries('select', 'transaccion', fields=['items','tipo'], where=['id'], where_value=[id_transaction], operators=['='], fetch=0)
    if data_transaction['items'] != ('[]',):
        new_data_transaction = eval(data_transaction['items'])

    #=============== Verificando si se esta intentando agregar un producto que ya existe en la venta ===============#
        for dic in new_data_transaction:
            if dic["codigo"] == res_product["codigo"]:
                aux = 1

    #=============== En caso de que el producto ya este no lo agregara, si no lo esta comprobara disponibilidad =================#
        if aux == 1:
            return 'Producto ya agregado a la venta'
        else:
            new_data_transaction.append(res_product)
            cantidad_can = updateInventory(code, cant, True if data_transaction['tipo'] == 'venta' else False)
            if data_transaction['tipo'] == 'venta':
                if not cantidad_can:
                    return f'No hay suficiente stock del {code} para satisfacer la demanda'

    if not new_data_transaction:
        new_data_transaction.append(res_product)
        if data_transaction['tipo'] == 'venta':
            cantidad_can = updateInventory(code, cant, True)
            if not cantidad_can:
                return f'No hay suficiente stock del {code} para satisfacer la demanda'
        else:
            cantidad_can = updateInventory(code, cant, False)

    #=============== Actualizando la venta con el nuevo item ===============#
    db_queries('update', 'transaccion', items=f"""{new_data_transaction}""", where=['id'], where_value=[id_transaction], operators=['='])

    #=============== Actualizando total de la venta ===============#
    updateTotalCV(id_transaction, data_transaction['tipo'])
    return f'El Producto {code} fue Agregado'

@flask_routes.route('/transactions', methods=['GET'])
def getTransaction():
    data = db_queries('select', 'transaccion', fields=['*'])
    return jsonify(data)

@flask_routes.route('/transaction/<id>', methods=['GET'])
def getOneTransaction(id):
    data = db_queries('select', 'transaccion', where=['id'], where_value=[id], operators=['='], fields=['*'], fetch=0)
    return jsonify(data)

@flask_routes.route('/transactions/<id>', methods=['DELETE'])
def deleteTransaction(id):
    #=============== Aumentando el inventario con las cantidades eliminadas ===============#
    data_transaction= db_queries('select', 'transaccion', where=['id'], where_value=[id], operators=['='], fields=['items','tipo'], fetch=0)

    if data_transaction['items'] != ('[]',):
        new_data_transaction = eval(data_transaction['items'])

        for dic in new_data_transaction:
            updateInventory(dic["codigo"], dic['cantidad'], False if data_transaction['tipo'] == 'venta' else True)

    #=============== Actualizando la deuda ===============#
    deleteDeudaCV(id)

    #=============== Eliminando la venta ===============#
    db_queries('delete', 'transaccion', where=['id'], where_value=[id], operators=['='])
    return f'Venta #{id} Eliminada'

@flask_routes.route('/transactions/<code>/<id_transaction>', methods=['DELETE'])
def deleteItems(code, id_transaction):
    #=============== Verificando si la venta ya tiene items agregados ===============#
    data_transaction = db_queries('select', 'transaccion', where=['id'], where_value=[id_transaction], operators=['='], fields=['items','tipo'], fetch=0)

    if data_transaction['items'] != ('[]',):
        new_data_transaction = eval(data_transaction['items'])

        for dic in new_data_transaction:
            if dic["codigo"] == code:
                updateInventory(code, dic['cantidad'], False if data_transaction['tipo'] == 'venta' else True)
                new_data_transaction.pop(new_data_transaction.index(dic))

                #=============== Actualizando la venta sin el item eliminado ===============#
                db_queries('update', 'transaccion', where=['id'], where_value=[id_transaction], operators=['='],
                    items=f"""{new_data_transaction}"""
                )

                #=============== Actualizando total de la venta ===============#
                updateTotalCV(id_transaction, data_transaction['tipo'])
                return f'El Producto {code} Eliminado'
        return f'No se ha encontrado el {code} que desea eliminar'
    return f'No hay ningun producto para eliminar'

@flask_routes.route('/transactions/<id>', methods=['PUT'])
def updateTransaction(id):
    transaction = request.json
    res = db_queries('select', 'transaccion', where=['id'], where_value=[id], operators=['='], fields=['*'], fetch=0)

    db_queries('update', 'transaccion', where=['id'], where_value=[id], operators=['='],
        deudor = f"""{transaction["deudor"]}""", 
        acreedor = f"""{transaction["acreedor"]}""", 
        plazo = transaction["plazo"]
    )

    if (transaction["deudor"] != res["deudor"] 
        or transaction["acreedor"] != res["acreedor"] 
        or transaction["plazo"] != res["plazo"]):

        updateDeudaCV(res['tipo'], res["deudor"], res["acreedor"])
        updateDeudaCV(transaction['tipo'], transaction["deudor"], transaction["acreedor"])

    return f'Transaccion #{id} Actualizada'

@flask_routes.route('/transactions/<code>/<cant>/<id_sale>', methods=['PUT'])
def updateItem(code, cant, id_transaction):
    #=============== Verificando si la venta ya tiene items agregados ===============#
    data_transaction = db_queries('select', 'transaccion', where=['id'], where_value=id_transaction, fields=['items','tipo'], fetch=0)
    
    if data_transaction['items'] != ('[]',):
        new_data_transaction = eval(data_transaction['items'])

    #=============== Verificando si el producto que ya existe en la venta ===============#
        for dic in new_data_transaction:
            if dic["codigo"] == code:
                dic["cantidad"] = int(cant)
                dic["subtotal"] = dic["precio_venta"] * dic["cantidad"]

            #=============== Actualizando los items de la venta ===============#
                db_queries('update', 'transaccion', where=['id'], where_value=[id_transaction], operators=['='],
                    items = f"""{new_data_transaction}"""
                )

            #=============== Actualizando total de la venta ===============#
                updateTotalCV(id_transaction, data_transaction['tipo'])

                return f'Item {code} Actualizado'
            return f'No se encuentra el producto {code}'