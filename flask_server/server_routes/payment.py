from flask import request, jsonify
from flask_cors import CORS
from utilities.functions import *
from __init__ import routes
import datetime

#=============== Payments ===============#

@routes.route('/payments', methods=['POST'])
def createPayment():
    payment = request.json
    date = datetime.datetime.now()

    #=============== Consultando la informacion de contacto para buscar la deuda_contra ===============#
    query = f"""SELECT * FROM contacto WHERE documento = "{payment["documento_contacto"]}";"""
    data = get_db_connection(query, op=False)
    res = json_contact(data)

    #=============== Creando el Pago ===============#
    query = f"""INSERT INTO abono (documento_contacto, cant_abono, fecha) 
            VALUES ("{payment["documento_contacto"]}", {payment["cant_abono"]}, 
            "{date.strftime("%Y/%m/%d")}");"""
    get_db_connection(query)

    #=============== Actualizando contacto con la resta de la deuda_contra actual y el abono ===============#
    deuda_contra = res["deuda_contra"]-payment["cant_abono"]
    query = f"""UPDATE contacto SET deuda_contra = {deuda_contra} WHERE 
            id = {res["id"]};"""
    get_db_connection(query)
    return 'Pago Creado'

@routes.route('/payments', methods=['GET'])
def getPayment():
    query = f"SELECT * FROM abono;"
    data = get_db_connection(query, op=True)
    res = json_payment(data)
    return jsonify(res)

@routes.route('/payment/<id>', methods=['GET'])
def getOnePayment(id):
    query = f"SELECT * FROM abono WHERE id = {id};"
    data = get_db_connection(query, op=False)
    res = json_payment(data)
    return jsonify(res)

@routes.route('/payments/<id>', methods=['DELETE'])
def deletePayments(id):
    payment = request.json

    #=============== Consultando la informacion de contacto para buscar la deuda_contra ===============#
    query = f"""SELECT * FROM contacto WHERE documento = "{payment["documento_contacto"]}";"""
    data = get_db_connection(query, op=False)
    res = json_contact(data)

    #=============== Actualizando contacto con la suma de la deuda_contra actual y el abono eliminado ===============#
    deuda_contra = payment["cant_abono"] + res["deuda_contra"]
    query = f"""UPDATE contacto SET deuda_contra = {deuda_contra} WHERE 
            id = {res["id"]};"""
    get_db_connection(query)

    #=============== Eliminando el Pago ===============#
    query = f"DELETE FROM abono WHERE id = {id};"
    get_db_connection(query)
    return 'Pago Eliminado'

@routes.route('/payments/<id>', methods=['PUT'])
def updatePayment(id):
    payment = request.json
    date = datetime.datetime.now()

    #=============== Consultando la informacion de abono para buscar la cant_abono antes de actualizar ===============#
    query = f"SELECT * FROM abono WHERE id = {id};"
    cant_actual = get_db_connection(query, op=False)
    cant_actual = json_payment(cant_actual)

    #=============== Consultando la informacion de contacto para buscar la deuda_contra ===============#
    query = f"""SELECT * FROM contacto WHERE documento = "{payment["documento_contacto"]}";"""
    data_contact = get_db_connection(query, op=False)
    data_contact = json_contact(data_contact)

    #=============== Esta funcion realizala una operacion dependiendo si cant_actual es menor o mayor que cant_abono ===============#
    deuda_contra = updateAbono(cant_actual["cant_abono"], payment["cant_abono"], data_contact["deuda_contra"])

    #=============== Actualizando contacto con la operacion de la deuda_contra actual y el abono actualizado ===============#
    query = f"""UPDATE contacto SET deuda_contra = {deuda_contra} WHERE 
            id = "{data_contact["id"]}";"""
    get_db_connection(query)

    #=============== Actualizando el Pago ===============#
    query = f"""UPDATE abono SET documento_contacto = "{payment["documento_contacto"]}", 
            cant_abono = {payment["cant_abono"]}, fecha = "{date.strftime("%Y/%m/%d")}" WHERE id = {id};"""
    get_db_connection(query)
    return 'Pago Actualizado'
