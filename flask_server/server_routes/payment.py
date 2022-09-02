from flask import request, jsonify
from utilities.functions import *
from utilities.db_queries import db_queries
from __init__ import flask_routes
import datetime

#=============== Payments ===============#

@flask_routes.route('/payments', methods=['POST'])
def createPayment():
    payment = request.json
    date = datetime.datetime.now()

    #=============== Consultando la informacion de la venta para buscar el total ===============#
    data = db_queries('select', f"""{payment["origen"]}""", where='id', where_value=payment["id_origen"], fields=['*'], fetch=0)
    res_origen = json_sale(data)

    if (res_origen["total"] - res_origen["cantidad_pagada"]) >= payment["cant_abono"]:

        data = db_queries('select', 'contacto', where='documento', where_value=res_origen["deudor"], fields=['*'], fetch=0)
        res_deudor = json_contact(data)

        data = db_queries('select', 'contacto', where='documento', where_value=res_origen["acreedor"], fields=['*'], fetch=0)
        res_acreedor = json_contact(data)

        #=============== Creando el Pago ===============#
        db_queries('insert', 'pago', 
                id_origen = payment["id_origen"], 
                origen = f"""{payment["origen"]}""", 
                cant_abono = payment["cant_abono"], 
                fecha = f"""{date.strftime("%Y/%m/%d")}"""
        )

        #=============== Actualizando contacto con la resta de la deuda actual y el pago ===============#
        deuda_value = res_deudor["deuda"]-payment["cant_abono"]

        db_queries('update', 'contacto', where='documento', where_value=res_origen["deudor"],
                deuda = deuda_value
        )

        #=============== Actualizando contacto con la res_origen de la credito actual y el pago ===============#
        credito_value = res_acreedor["credito"]-payment["cant_abono"]

        db_queries('update', 'contacto', where='documento', where_value=res_origen["acreedor"],
                credito = credito_value
        )

        cant_pagada = res_origen["cantidad_pagada"] + payment["cant_abono"]

        db_queries('update', 'venta', where='id', where_value=res_origen["id"],
                cantidad_pagada = cant_pagada
        )

        return 'Pago Creado'
    return f'La cantidad pagada debe ser menor o igual a {res_origen["total"]-res_origen["cantidad_pagada"]}' if res_origen["total"]-res_origen["cantidad_pagada"] != 0 else f'La venta ha sido pagada por completo'

@flask_routes.route('/payments', methods=['GET'])
def getPayment():
    data = db_queries('select', 'pago', fields=['*'], fetch=1)
    res = json_payment(data)
    return jsonify(res)

@flask_routes.route('/payment/<id>', methods=['GET'])
def getOnePayment(id):
    data = db_queries('select', 'pago', where='id', where_value=id, fields=['*'], fetch=0)
    res = json_payment(data)
    return jsonify(res)

@flask_routes.route('/payments/<id>', methods=['DELETE'])
def deletePayments(id):

    data = db_queries('select', 'pago', where='id', where_value=id, fields=['*'], fetch=0)
    payment = json_payment(data)

    #=============== Consultando la informacion de la venta para buscar el total ===============#
    data = db_queries('select', f"""{payment["origen"]}""", where='id', where_value=payment["id_origen"], fields=['*'], fetch=0)
    res_origen = json_sale(data)

    data = db_queries('select', 'contacto', where='documento', where_value=res_origen["deudor"], fields=['*'], fetch=0)
    res_deudor = json_contact(data)

    data = db_queries('select', 'contacto', where='documento', where_value=res_origen["acreedor"], fields=['*'], fetch=0)
    res_acreedor = json_contact(data)

    #=============== Actualizando contacto con la resta de la deuda actual y el pago ===============#
    deuda_value = res_deudor["deuda"]+payment["cant_abono"]

    db_queries('update', 'contacto', where='documento', where_value=res_origen["deudor"],
             deuda = deuda_value
    )

    #=============== Actualizando contacto con la res_origen de la credito actual y el pago ===============#
    credito_value = res_acreedor["credito"]+payment["cant_abono"]

    db_queries('update', 'contacto', where='documento', where_value=res_origen["acreedor"],
            credito = credito_value
    )

    cant_pagada = res_origen["cantidad_pagada"]-payment["cant_abono"]

    db_queries('update', 'venta', where='id', where_value=res_origen["id"],
            cantidad_pagada = cant_pagada
     )

    db_queries('delete', 'pago', where='id', where_value=id)

    return 'Pago Eliminado'

@flask_routes.route('/payments/<id>', methods=['PUT'])
def updatePayment(id):
    payment = request.json

    res_origen = db_queries('select', f"""{payment["origen"]}""", where='id', where_value=payment["id_origen"], fields=['*'], fetch=0)
    res_origen = json_sale(res_origen)

    #=============== Consultando la informacion de pago ===============#
    cant_actual = db_queries('select', 'pago', where='id', where_value=id, fields=['*'], fetch=0)
    cant_actual = json_payment(cant_actual)

    if payment["cant_abono"] + (res_origen["cantidad_pagada"] - cant_actual["cant_abono"]) <= res_origen["total"]:
        #=============== Consultando la informacion de contacto ===============#
        data_contact = db_queries('select', 'contacto', where='documento', where_value=res_origen["deudor"], fields=['*'], fetch=0)
        data_contact = json_contact(data_contact)

        data_acreedor = db_queries('select', 'contacto', where='documento', where_value=res_origen["acreedor"], fields=['*'], fetch=0)
        data_acreedor = json_contact(data_acreedor)

        #=============== Esta funcion realizala una operacion dependiendo si cant_actual es menor o mayor que cant_abono ===============#
        deuda_value = updateAbono(cant_actual["cant_abono"], payment["cant_abono"], data_contact["deuda"])

        credito_value = updateAbono(cant_actual["cant_abono"], payment["cant_abono"], data_acreedor["credito"])

        #=============== Actualizando contactos ===============#
        db_queries('update', 'contacto', where='id', where_value=data_contact["id"],
                deuda= deuda_value
        )

        db_queries('update', 'contacto', where='id', where_value=data_acreedor["id"],
                credito= credito_value
        )

        if cant_actual["cant_abono"] >= payment["cant_abono"]:
                cant_pagada = res_origen["cantidad_pagada"] - (cant_actual["cant_abono"] - payment["cant_abono"])
        else:
                cant_pagada = res_origen["cantidad_pagada"] + (payment["cant_abono"] - cant_actual["cant_abono"])

        #=============== Actualizando Venta ===============#
        db_queries('update', 'venta', where='id', where_value=res_origen["id"],
                cantidad_pagada = cant_pagada
        )

        #=============== Actualizando el Pago ===============#
        db_queries('update', 'pago', where='id', where_value=id,
                cant_abono = payment["cant_abono"]
        )

        return 'Pago Actualizado'
    return f'La cantidad pagada no puede ser mayor a {res_origen["total"] - (res_origen["cantidad_pagada"] - cant_actual["cant_abono"])}'
