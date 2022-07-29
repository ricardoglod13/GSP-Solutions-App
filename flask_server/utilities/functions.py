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
                    "deuda_favor": tupla[5],
                    "deuda_contra": tupla[6],
                    "tipo": tupla[7]
                })
            return contacts

        contact = {
                "id": data[0],
                "documento":data[1],
                "nombre": data[2],
                "telefono": data[3],
                "direccion": data[4],
                "deuda_favor": data[5],
                "deuda_contra": data[6],
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
                    "documento_contacto":tupla[1],
                    "documento_sucursal": tupla[2],
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
                "documento_contacto":data[1],
                "documento_sucursal": data[2],
                "items": data[3],
                "pago_inmediato": data[4],
                "cantidad_pagada": data[5],
                "total": total,
                "fecha": data[7]
            }
        return sale

def json_sale_product(data, cant):
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

def updateTotalVenta(id):
    #=============== Obteniendo la venta donde se debe carcular el total ===============#
    data = db_queries('select', 'venta', where='id', where_value=id, fields=['*'], fetch=0)
    res = json_sale(data)

    #================ Actualizando el total de la venta ===============#
    db_queries('update', 'venta', where='id', where_value=id,
        total= res["total"]
    )

    #================ Actualizando la deuda_contra y deuda_favor de el cliente y la sucursal ===============#
    updateDeudaVenta(res["documento_contacto"], res["documento_sucursal"])

def updateDeudaVenta(documento, documento_sucursal):
    #=============== Obteniendo el total de todas las compras ===============#
    data_total = db_queries('select', 'venta', where='documento_contacto', where_value=documento, fields=['*'], fetch=1)
    deuda_total = calculateTotal(data_total)

    #=============== Actualizando la deuda del contacto con las compras que no hayan sido pago inmediato ===============#
    db_queries('update', 'contacto', where='documento', where_value=documento,
        deuda_contra= deuda_total
    )

    #=============== Obteniendo el total de todas las ventas ===============#
    data_total_sucursal = db_queries('select', 'venta', where='documento_sucursal', where_value=documento_sucursal, fields=['*'], fetch=1)
    deuda_total_sucursal = calculateTotal(data_total_sucursal)

    #=============== Actualizando el total del contacto con las compras que no hayan sido pago inmediato ===============#
    db_queries('update', 'contacto', where='documento', where_value=documento_sucursal,
        deuda_favor= deuda_total_sucursal
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
    for val in deuda:
        print(val) 
    print(f"""sum={sum(deuda)}""")

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

def deleteDeudaVenta(id):
    deuda_contra = 0

    #=============== Obteniendo el total de la venta ===============#
    data_total = db_queries('select', 'venta', where='id', where_value=id, fields=['*'], fetch=0)
    res = json_sale(data_total)

    #=============== Obteniendo la deuda_contra del contacto que realiza la compra ===============#
    data_deuda_contra = db_queries('select', 'contacto', where='documento', where_value=res["documento_contacto"], fields=['deuda_contra'], fetch=0)

    deuda_contra_value = data_deuda_contra[0] - res["total"]

    db_queries('update', 'contacto', where='documento', where_value=res["documento_contacto"], 
                deuda_contra= deuda_contra_value
            )

    #=============== Obteniendo la deuda_favor de la sucursal que realiza la venta ===============#
    data_deuda_sucursal = db_queries('select', 'contacto', where='documento', where_value=res["documento_sucursal"], fields=['deuda_favor'], fetch=0)

    deuda_favor_value = data_deuda_sucursal[0] - res["total"]

    db_queries('update', 'contacto', where='documento', where_value=res["documento_sucursal"], 
                deuda_favor= deuda_favor_value
            )

def updateAbono(cant_actual, cant_abono, deuda):
    if cant_actual > cant_abono:
        deuda = (cant_actual-cant_abono) + deuda
        return deuda

    deuda = deuda - (cant_abono-cant_actual)
    return deuda
