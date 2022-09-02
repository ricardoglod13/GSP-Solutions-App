from flask import request, jsonify
from utilities.functions import *
from utilities.db_queries import db_queries
from __init__ import flask_routes
import datetime

#=============== Purchases ===============#

@flask_routes.route('/purchases', methods=['POST'])
def createPurchase():
    purchase = request.json
    date = datetime.datetime.now()
    db_queries('insert', 'compra', 
        deudor = f"""{purchase["deudor"]}""",
        acreedor = f"""{purchase["acreedor"]}""",
        items = f"""[]""", 
        pago_inmediato = purchase["pago_inmediato"],
        cantidad_pagada = 0,
        total = 0.0,
        fecha = f"""{date.strftime("%Y/%m/%d")}"""
    )
    return 'Compra creada'

@flask_routes.route('/purchases/<code>/<cant>/<id_purchase>', methods=['POST'])
def addItemsP(code, cant, id_purchase):
    new_data_purchase = []
    aux = 0

    #============== Seleccionando el producto ===============#
    data_product = db_queries('select', 'producto', where='codigo', where_value=code, fields=['*'], fetch=0)
    res_product = json_ps_product(data_product, cant)

    #=============== Verificando si la compra ya tiene items agregados ===============#
    data_purchase = db_queries('select', 'compra', fields=['items'], where='id', where_value=id_purchase, fetch=0)
    if data_purchase != ('[]',):
        new_data_purchase = eval(data_purchase[0])

    #=============== Verificando si se esta intentando agregar un producto que ya existe en la compra ===============#
        for dic in new_data_purchase:
            if dic["codigo"] == res_product["codigo"]:
                aux = 1

    #=============== En caso de que el producto ya este no lo agregara, si no lo esta comprobara disponibilidad =================#
        if aux == 1:
            return 'Producto ya agregado a la compra'
        else:
            new_data_purchase.append(res_product)
            updateInventory(code, cant, False)

    if not new_data_purchase:
        new_data_purchase.append(res_product)
        updateInventory(code, cant, False)

    #=============== Actualizando la compra con el nuevo item ===============#
    db_queries('update', 'compra', items=f"""{new_data_purchase}""", where='id', where_value=id_purchase)

    #=============== Actualizando total de la compra ===============#
    updateTotalCV(id_purchase, 'compra')
    return f'El Producto {code} fue Agregado a la compra!'

@flask_routes.route('/purchases', methods=['GET'])
def getPurchase():
    data = db_queries('select', 'compra', fields=['*'])
    res = json_purchase(data)
    return jsonify(res)

@flask_routes.route('/purchase/<id>', methods=['GET'])
def getOnePurchase(id):
    data = db_queries('select', 'compra', where='id', where_value=id, fields=['*'], fetch=0)
    res = json_purchase(data)
    return jsonify(res)

@flask_routes.route('/purchases/<id>', methods=['DELETE'])
def deletePurchase(id):
    #=============== Aumentando el incomprario con las cantidades eliminadas ===============#
    data_purchase= db_queries('select', 'compra', where='id', where_value=id, fields=['items'], fetch=0)

    if data_purchase != ('[]',):
        new_data_purchase = eval(data_purchase[0])

        for dic in new_data_purchase:
            updateInventory(dic["codigo"], dic['cantidad'], True)

    #=============== Actualizando la deuda ===============#
    deleteDeudaCV(id, 'compra')

    #=============== Eliminando la compra ===============#
    db_queries('delete', 'compra', where='id', where_value=id)
    return f'compra #{id} Eliminada'

@flask_routes.route('/purchases/<code>/<id_purchase>', methods=['DELETE'])
def deleteItemsP(code, id_purchase):
    #=============== Verificando si la compra ya tiene items agregados ===============#
    data_purchase = db_queries('select', 'compra', where='id', where_value=id_purchase, fields=['items'], fetch=0)

    if data_purchase != ('[]',):
        new_data_purchase = eval(data_purchase[0])

        for dic in new_data_purchase:
            if dic["codigo"] == code:
                updateInventory(code, dic['cantidad'], True)
                new_data_purchase.pop(new_data_purchase.index(dic))

                #=============== Actualizando la compra sin el item eliminado ===============#
                db_queries('update', 'compra', where='id', where_value=id_purchase,
                    items=f"""{new_data_purchase}"""
                )

                #=============== Actualizando total de la compra ===============#
                updateTotalCV(id_purchase, 'compra')
                return f'El Producto {code} Eliminado de la compra!'
        return f'No se ha encontrado el {code} que desea eliminar'
    return f'No hay ningun producto para eliminar'

@flask_routes.route('/purchases/<id>', methods=['PUT'])
def updatePurchase(id):
    purchase = request.json
    data = db_queries('select', 'compra', where='id', where_value=id, fields=['*'], fetch=0)
    res = json_purchase(data)

    db_queries('update', 'compra', where='id', where_value=id,
        deudor = f"""{purchase["deudor"]}""", 
        acreedor = f"""{purchase["acreedor"]}""", 
        pago_inmediato = purchase["pago_inmediato"]
    )

    if (purchase["deudor"] != res["deudor"] 
        or purchase["acreedor"] != res["acreedor"] 
        or purchase["pago_inmediato"] != res["pago_inmediato"]):

        updateDeudaCV('compra', res["deudor"], res["acreedor"])
        updateDeudaCV('compra', purchase["deudor"], purchase["acreedor"])

    return f'Compra #{id} Actualizada'

@flask_routes.route('/purchases/<code>/<cant>/<id_purchase>', methods=['PUT'])
def updateItemP(code, cant, id_purchase):
    #=============== Verificando si la compra ya tiene items agregados ===============#
    data_purchase = db_queries('select', 'compra', where='id', where_value=id_purchase, fields=['items'], fetch=0)
    
    if data_purchase != ('[]',):
        new_data_purchase = eval(data_purchase[0])

    #=============== Verificando si el producto que ya existe en la compra ===============#
        for dic in new_data_purchase:
            if dic["codigo"] == code:
                dic["cantidad"] = int(cant)
                dic["subtotal"] = dic["precio_venta"] * dic["cantidad"]

            #=============== Actualizando los items de la compra ===============#
                db_queries('update', 'compra', where='id', where_value=id_purchase,
                    items = f"""{new_data_purchase}"""
                )

            #=============== Actualizando total de la compra ===============#
                updateTotalCV(id_purchase, 'compra')

                return f'Item {code} Actualizado'
            return f'No se encuentra el producto {code}'