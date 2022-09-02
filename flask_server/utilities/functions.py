from .db_queries import db_queries

def json_product(data):
    tipo = isinstance(data, list)
    if data:
        if tipo == True:
            products = []
            for tupla in data:
                products.append({
                    "id": tupla[0],
                    "codigo": tupla[1],
                    "tipo": tupla[2],
                    "descripcion": tupla[3],
                    "precio_costo": tupla[4],
                    "precio_venta": tupla[5],
                    "cantidad": tupla[6]
                })
            return products

        product = {
                "id": data[0],
                "codigo": data[1],
                "tipo": data[2],
                "descripcion": data[3],
                "precio_costo": data[4],
                "precio_venta": data[5],
                "cantidad": data[6]
            }
        return product

def json_contact(data):
    lista = isinstance(data, list)
    if data:
        if lista == True:
            contacts = []
            for tupla in data:
                contacts.append({
                    "id": tupla[0],
                    "documento":tupla[1],
                    "nombre": tupla[2],
                    "telefono": tupla[3],
                    "direccion": tupla[4],
                    "credito": tupla[5],
                    "deuda": tupla[6],
                    "tipo": tupla[7]
                })
            return contacts

        contact = {
                "id": data[0],
                "documento":data[1],
                "nombre": data[2],
                "telefono": data[3],
                "direccion": data[4],
                "credito": data[5],
                "deuda": data[6],
                "tipo": data[7]
            }
        return contact

def json_payment(data):
    tipo = isinstance(data, list)
    if data:
        if tipo == True:
            payments = []
            for tupla in data:
                payments.append({
                    "id": tupla[0],
                    "id_origen":tupla[1],
                    "origen": tupla[2],
                    "cant_abono": tupla[3],
                    "fecha": tupla[4]
                })
            return payments

        payment = {
                "id": data[0],
                "id_origen":data[1],
                "origen": data[2],
                "cant_abono": data[3],
                "fecha": data[4]
            }
        return payment

def json_sale(data):
    tipo = isinstance(data, list)
    total = 0
    if data:
        if tipo == True:
            sales = []
            for tupla in data:
                total = 0
                lista = eval(tupla[3])
                for dic in lista:
                    total = dic["subtotal"] + total
                sales.append({
                    "id": tupla[0],
                    "deudor":tupla[1],
                    "acreedor": tupla[2],
                    "items": tupla[3],
                    "pago_inmediato": tupla[4],
                    "cantidad_pagada": tupla[5],
                    "total": total,
                    "fecha": tupla[7]
                })
            return sales

        dic = eval(data[3])
        for element in dic:
            total = element["subtotal"] + total
        sale = {
                "id": data[0],
                "deudor":data[1],
                "acreedor": data[2],
                "items": data[3],
                "pago_inmediato": data[4],
                "cantidad_pagada": data[5],
                "total": total,
                "fecha": data[7]
            }
        return sale

def json_purchase(data):
    tipo = isinstance(data, list)
    total = 0
    if data:
        if tipo == True:
            purchases = []
            for tupla in data:
                total = 0
                lista = eval(tupla[3])
                for dic in lista:
                    total = dic["subtotal"] + total
                purchases.append({
                    "id": tupla[0],
                    "deudor":tupla[1],
                    "acreedor": tupla[2],
                    "items": tupla[3],
                    "pago_inmediato": tupla[4],
                    "cantidad_pagada": tupla[5],
                    "total": total,
                    "fecha": tupla[7]
                })
            return purchases

        dic = eval(data[3])
        for element in dic:
            total = element["subtotal"] + total
        purchase = {
                "id": data[0],
                "deudor":data[1],
                "acreedor": data[2],
                "items": data[3],
                "pago_inmediato": data[4],
                "cantidad_pagada": data[5],
                "total": total,
                "fecha": data[7]
            }
        return purchase

def json_ps_product(data, cant):
    if data:
        product = {
                "id": data[0],
                "codigo": data[1],
                "tipo": data[2],
                "descripcion": data[3],
                "precio_venta": data[5],
                "cantidad": int(cant),
                "subtotal": data[5]*int(cant)
            }
        return product

def updateTotalCV(id, tabla):
    #=============== Obteniendo la venta donde se debe carcular el total ===============#
    if tabla == 'venta':
        data = db_queries('select', 'venta', where='id', where_value=id, fields=['*'], fetch=0)
        res = json_sale(data)

        #================ Actualizando el total de la venta ===============#
        db_queries('update', 'venta', where='id', where_value=id,
            total= res["total"]
        )

        #================ Actualizando la deuda y credito de el cliente y la acreedor ===============#
        updateDeudaCV(f'{tabla}', res["deudor"], res["acreedor"])

    elif tabla == 'compra':
        data = db_queries('select', 'compra', where='id', where_value=id, fields=['*'], fetch=0)
        res = json_purchase(data)

        #================ Actualizando el total de la venta ===============#
        db_queries('update', 'compra', where='id', where_value=id,
            total= res["total"]
        )

        #================ Actualizando la deuda y credito de el cliente y la acreedor ===============#
        updateDeudaCV(f'{tabla}', res["deudor"], res["acreedor"])    

def updateDeudaCV(tabla, documento_deudor, documento_acreedor):
    #=============== Obteniendo el total de todas las compras ===============#
    if tabla == 'venta':
        data_total = db_queries('select', 'venta', where='deudor', where_value=documento_deudor, fields=['*'], fetch=1)
    elif tabla == 'compra':
        data_total = db_queries('select', 'compra', where='deudor', where_value=documento_deudor, fields=['*'], fetch=1)
    deuda_total = calculateTotal(data_total)

    #=============== Actualizando la deuda del contacto con las compras que no hayan sido pago inmediato ===============#
    db_queries('update', 'contacto', where='documento', where_value=documento_deudor,
        deuda= deuda_total
    )

    #=============== Obteniendo el total de todas las ventas ===============#
    if tabla == 'venta':
        data_total_acreedor = db_queries('select', 'venta', where='acreedor', where_value=documento_acreedor, fields=['*'], fetch=1)
    elif tabla == 'compra':
        data_total_acreedor = db_queries('select', 'compra', where='acreedor', where_value=documento_acreedor, fields=['*'], fetch=1)
    data_total_acreedor = calculateTotal(data_total_acreedor)

    #=============== Actualizando el total del contacto con las compras que no hayan sido pago inmediato ===============#
    db_queries('update', 'contacto', where='documento', where_value=documento_acreedor,
        credito= data_total_acreedor
    )

def calculateTotal(data):
    deuda = []
    for tupla in data:
        total = 0
        items = tupla[3]
        pago_inmediato = tupla[4]
        if items:
            products = eval(items)
            if not pago_inmediato:
                for dic in products:
                    total = dic["subtotal"] + total
            deuda.append(total) 

    deuda_total = sum(deuda)

    return deuda_total

def updateInventory(code, cant, op):
    #=============== Obteniendo la cantidad del producto agregado ===============#
    data_cant = db_queries('select', 'producto', where='codigo', where_value=code, fields=['cantidad'], fetch=0)
    
    if op:
        if data_cant[0] >= int(cant):
            db_queries('update', 'producto', where='codigo', where_value=code, 
                cantidad= data_cant[0]-int(cant)
            )
            return True
        return False
    else:
        db_queries('update', 'producto', where='codigo', where_value=code, 
                cantidad= data_cant[0]+int(cant)
            )

def deleteDeudaCV(id, tabla):

    if tabla == 'venta':
        #=============== Obteniendo el total de la venta ===============#
        data_total = db_queries('select', 'venta', where='id', where_value=id, fields=['*'], fetch=0)
        res = json_sale(data_total)

        #=============== Obteniendo la deuda del contacto que realiza la compra ===============#
        data_deuda = db_queries('select', 'contacto', where='documento', where_value=res["deudor"], fields=['deuda'], fetch=0)

        deuda_value = data_deuda[0] - res["total"]

        db_queries('update', 'contacto', where='documento', where_value=res["deudor"], 
                    deuda= deuda_value
                )

        #=============== Obteniendo la credito de la acreedor que realiza la venta ===============#
        data_deuda_acreedor = db_queries('select', 'contacto', where='documento', where_value=res["acreedor"], fields=['credito'], fetch=0)

        credito_value = data_deuda_acreedor[0] - res["total"]

        db_queries('update', 'contacto', where='documento', where_value=res["acreedor"], 
                    credito= credito_value
                )

    elif tabla == 'compra':
        #=============== Obteniendo el total de la venta ===============#
        data_total = db_queries('select', 'compra', where='id', where_value=id, fields=['*'], fetch=0)
        res = json_purchase(data_total)

        #=============== Obteniendo la deuda del contacto que realiza la compra ===============#
        data_deuda = db_queries('select', 'contacto', where='documento', where_value=res["deudor"], fields=['deuda'], fetch=0)

        deuda_value = data_deuda[0] - res["total"]

        db_queries('update', 'contacto', where='documento', where_value=res["deudor"], 
                    deuda= deuda_value
                )

        #=============== Obteniendo la credito del acreedor que realiza la venta ===============#
        data_deuda_proveedor = db_queries('select', 'contacto', where='documento', where_value=res["acreedor"], fields=['credito'], fetch=0)

        credito_value = data_deuda_proveedor[0] - res["total"]

        db_queries('update', 'contacto', where='documento', where_value=res["acreedor"], 
                    credito= credito_value
                )

def updateAbono(cant_actual, cant_abono, deuda):
    if cant_actual > cant_abono:
        deuda = (cant_actual-cant_abono) + deuda
        return deuda

    deuda = deuda - (cant_abono-cant_actual)
    return deuda
