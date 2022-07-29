from flask import request, jsonify
from flask_cors import CORS
from utilities.functions import *
from utilities.db_queries import db_queries
from __init__ import flask_routes
import datetime

#=============== Sales ===============#

@flask_routes.route('/sales', methods=['POST'])
def createSale():
    sale = request.json
    date = datetime.datetime.now()
    db_queries('insert', 'venta', 
        documento_contacto = f"""{sale["documento_contacto"]}""",
        documento_sucursal = f"""{sale["documento_sucursal"]}""", 
        items = f"""[]""", 
        pago_inmediato = sale["pago_inmediato"],
        cantidad_pagada = 0,
        total = 0.0,
        fecha = f"""{date.strftime("%Y/%m/%d")}"""
    )
    return 'Venta creada'

@flask_routes.route('/sales/<code>/<cant>/<id_sale>', methods=['POST'])
def addItems(code, cant, id_sale):
    new_data_sale = []
    aux = 0

    #============== Seleccionando el producto ===============#
    data_product = db_queries('select', 'producto', where='codigo', where_value=code, fields=['*'], fetch=0)
    res_product = json_sale_product(data_product, cant)

    #=============== Verificando si la venta ya tiene items agregados ===============#
    data_sale = db_queries('select', 'venta', fields=['items'], where='id', where_value=id_sale, fetch=0)
    if data_sale != ('[]',):
        new_data_sale = eval(data_sale[0])

    #=============== Verificando si se esta intentando agregar un producto que ya existe en la venta ===============#
        for dic in new_data_sale:
            if dic["codigo"] == res_product["codigo"]:
                aux = 1

    #=============== En caso de que el producto ya este no lo agregara, si no lo esta comprobara disponibilidad =================#
        if aux == 1:
            return 'Producto ya agregado a la venta'
        else:
            new_data_sale.append(res_product)
            cantidad_can = updateInventory(code, cant, True)
            if not cantidad_can:
                return f'No hay suficiente stock del {code} para satisfacer la demanda'

    if not new_data_sale:
        new_data_sale.append(res_product)
        cantidad_can = updateInventory(code, cant, True)
        if not cantidad_can:
            return f'No hay suficiente stock del {code} para satisfacer la demanda'

    #=============== Actualizando la venta con el nuevo item ===============#
    db_queries('update', 'venta', items=f"""{new_data_sale}""", where='id', where_value=id_sale)

    #=============== Actualizando total de la venta ===============#
    updateTotalVenta(id_sale)
    return f'El Producto {code} fue Agregado a la Venta!'

@flask_routes.route('/sales', methods=['GET'])
def getSale():
    data = db_queries('select', 'venta', fields=['*'])
    res = json_sale(data)
    return jsonify(res)

@flask_routes.route('/sale/<id>', methods=['GET'])
def getOneSale(id):
    data = db_queries('select', 'venta', where='id', where_value=id, fields=['*'], fetch=0)
    res = json_sale(data)
    return jsonify(res)

@flask_routes.route('/sales/<id>', methods=['DELETE'])
def deleteSale(id):
    #=============== Aumentando el inventario con las cantidades eliminadas ===============#
    data_sale= db_queries('select', 'venta', where='id', where_value=id, fields=['items'], fetch=0)

    if data_sale != ('[]',):
        new_data_sale = eval(data_sale[0])

        for dic in new_data_sale:
            updateInventory(dic["codigo"], dic['cantidad'], False)

    #=============== Actualizando la deuda_contra ===============#
    deleteDeudaVenta(id)

    #=============== Eliminando la venta ===============#
    db_queries('delete', 'venta', where='id', where_value=id)
    return f'Venta #{id} Eliminada'

@flask_routes.route('/sales/<code>/<id_sale>', methods=['DELETE'])
def deleteItems(code, id_sale):
    #=============== Verificando si la venta ya tiene items agregados ===============#
    data_sale = db_queries('select', 'venta', where='id', where_value=id_sale, fields=['items'], fetch=0)

    if data_sale != ('[]',):
        new_data_sale = eval(data_sale[0])

        for dic in new_data_sale:
            if dic["codigo"] == code:
                updateInventory(code, dic['cantidad'], False)
                new_data_sale.pop(new_data_sale.index(dic))

                #=============== Actualizando la venta sin el item eliminado ===============#
                db_queries('update', 'venta', where='id', where_value=id_sale,
                    items=f"""{new_data_sale}"""
                )

                #=============== Actualizando total de la venta ===============#
                updateTotalVenta(id_sale)
                return f'El Producto {code} Eliminado de la Venta!'
        return f'No se ha encontrado el {code} que desea eliminar'
    return f'No hay ningun producto para eliminar'

@flask_routes.route('/sales/<id>', methods=['PUT'])
def updateSale(id):
    sale = request.json
    data = db_queries('select', 'venta', where='id', where_value=id, fields=['*'], fetch=0)
    res = json_sale(data)

    db_queries('update', 'venta', where='id', where_value=id,
        documento_contacto = f"""{sale["documento_contacto"]}""", 
        documento_sucursal = f"""{sale["documento_sucursal"]}""", 
        pago_inmediato = sale["pago_inmediato"]
    )

    if (sale["documento_contacto"] != res["documento_contacto"] 
        or sale["documento_sucursal"] != res["documento_sucursal"] 
        or sale["pago_inmediato"] != res["pago_inmediato"]):

        updateDeudaVenta(res["documento_contacto"], res["documento_sucursal"])
        updateDeudaVenta(sale["documento_contacto"], sale["documento_sucursal"])

    return f'Venta #{id} Actualizada'

@flask_routes.route('/sales/<code>/<cant>/<id_sale>', methods=['PUT'])
def updateItem(code, cant, id_sale):
    #=============== Verificando si la venta ya tiene items agregados ===============#
    data_sale = db_queries('select', 'venta', where='id', where_value=id_sale, fields=['items'], fetch=0)
    
    if data_sale != ('[]',):
        new_data_sale = eval(data_sale[0])

    #=============== Verificando si el producto que ya existe en la venta ===============#
        for dic in new_data_sale:
            if dic["codigo"] == code:
                dic["cantidad"] = int(cant)
                dic["subtotal"] = dic["precio_venta"] * dic["cantidad"]

            #=============== Actualizando los items de la venta ===============#
                db_queries('update', 'venta', where='id', where_value=id_sale,
                    items = f"""{new_data_sale}"""
                )

            #=============== Actualizando total de la venta ===============#
                updateTotalVenta(id_sale)

                return f'Item {code} Actualizado'
            return f'No se encuantra el producto {code}'