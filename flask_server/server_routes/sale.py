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
        total = 0.0, 
        fecha = f"""{date.strftime("%Y/%m/%d")}"""
    )
    return 'Venta creada'

@flask_routes.route('/sales/<code>/<cant>/<id_sale>', methods=['POST'])
def addItems(code, cant, id_sale):
    new_data_sale = []
    aux = 0

    #============== Seleccionando el producto ===============#
    data_product = db_queries('select', 'producto', where='codigo', where_value=code)
    res_product = json_sale_product(data_product, cant)

    #=============== Verificando si la venta ya tiene items agregados ===============#
    data_sale = db_queries('select', 'venta', fields=['items'], where='id', where_value=id_sale)
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
    data = db_queries('select', 'venta')
    res = json_sale(data)
    return jsonify(res)

@flask_routes.route('/sale/<id>', methods=['GET'])
def getOneSale(id):
    data = db_queries('select', 'venta', where='id', where_value=id)
    res = json_sale(data)
    return jsonify(res)

@flask_routes.route('/sales/<id>', methods=['DELETE'])
def deleteSale(id):
    #=============== Aumentando el inventario con las cantidades eliminadas ===============#
    query = f"""SELECT items FROM venta WHERE id = {id};"""
    data_sale = get_db_connection(query, op=False)

    if data_sale != ('[]',):
        new_data_sale = eval(data_sale[0])

        for dic in new_data_sale:
            updateInventory(dic["codigo"], dic['cantidad'], False)

    #=============== Actualizando la deuda_contra ===============#
    deleteDeudaVenta(id)

    #=============== Eliminando la venta ===============#
    query = f"DELETE FROM venta WHERE id = {id};"
    get_db_connection(query)
    return f'Venta #{id} Eliminada'

@flask_routes.route('/sales/<code>/<id_sale>', methods=['DELETE'])
def deleteItems(code, id_sale):
    #=============== Verificando si la venta ya tiene items agregados ===============#
    query = f"""SELECT items FROM venta WHERE id = {id_sale};"""
    data_sale = get_db_connection(query, op=False)

    if data_sale != ('[]',):
        new_data_sale = eval(data_sale[0])

        for dic in new_data_sale:
            if dic["codigo"] == code:
                updateInventory(code, dic['cantidad'], False)
                new_data_sale.pop(new_data_sale.index(dic))

                #=============== Actualizando la venta sin el item eliminado ===============#
                query = f"""UPDATE venta SET items = "{new_data_sale}" WHERE id = {id_sale};"""
                get_db_connection(query)

                #=============== Actualizando total de la venta ===============#
                updateTotalVenta(id_sale)
                return f'El Producto {code} Eliminado de la Venta!'
        return f'No se ha encontrado el {code} que desea eliminar'
    return f'No hay ningun producto para eliminar'

@flask_routes.route('/sales/<id>', methods=['PUT'])
def updateSale(id):
    sale = request.json
    query = f"SELECT * FROM venta WHERE id = {id};"
    data = get_db_connection(query, op=False)
    res = json_sale(data)

    query = f"""UPDATE venta SET documento_contacto = "{sale["documento_contacto"]}", 
            documento_sucursal = "{sale["documento_sucursal"]}", pago_inmediato = {sale["pago_inmediato"]}
            WHERE id = {id};"""
    get_db_connection(query)

    if (sale["documento_contacto"] != res["documento_contacto"] 
        or sale["documento_sucursal"] != res["documento_sucursal"] 
        or sale["pago_inmediato"] != res["pago_inmediato"]):

        updateDeudaVenta(res["documento_contacto"], res["documento_sucursal"])
        updateDeudaVenta(sale["documento_contacto"], sale["documento_sucursal"])

    return f'Venta #{id} Actualizada'

@flask_routes.route('/sales/<code>/<cant>/<id_sale>', methods=['PUT'])
def updateItem(code, cant, id_sale):
    #=============== Verificando si la venta ya tiene items agregados ===============#
    query = f"""SELECT items FROM venta WHERE id = {id_sale};"""
    data_sale = get_db_connection(query, op=False)
    
    if data_sale != ('[]',):
        new_data_sale = eval(data_sale[0])

    #=============== Verificando si el producto que ya existe en la venta ===============#
        for dic in new_data_sale:
            if dic["codigo"] == code:
                dic["cantidad"] = int(cant)
                dic["subtotal"] = dic["precio_venta"] * dic["cantidad"]

            #=============== Actualizando los items de la venta ===============#
                query = f"""UPDATE venta SET items = "{new_data_sale}" WHERE id = {id_sale};"""
                get_db_connection(query)

            #=============== Actualizando total de la venta ===============#
                updateTotalVenta(id_sale)

                return f'Item {code} Actualizado'