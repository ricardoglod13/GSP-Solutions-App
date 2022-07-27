import sqlite3

def get_db_connection(query, **kwargs):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute(f'{query}') 
    con.commit()
    if query[0:6] != "SELECT":
        con.close()
    elif kwargs.get('op'):
        data = cur.fetchall()
        con.close()
        return (data)
    elif not kwargs.get('op'):
        data = cur.fetchone()
        con.close()
        return (data)

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
                    "documento_contacto":tupla[1],
                    "cant_abono": tupla[2],
                    "fecha": tupla[3]
                })
            return payments

        payment = {
                "id": data[0],
                "documento_contacto":data[1],
                "cant_abono": data[2],
                "fecha": data[3]
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
                    "total": total,
                    "fecha": tupla[6]
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
                "total": total,
                "fecha": data[6]
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
    query = f"SELECT * FROM venta WHERE id = {id};"
    data = get_db_connection(query, op=False)
    res = json_sale(data)

    #================ Actualizando el total de la venta ===============#
    query = f"""UPDATE venta SET total = {res["total"]} WHERE id = {id};"""
    get_db_connection(query)

    #================ Actualizando la deuda_contra y deuda_favor de el cliente y la sucursal ===============#
    updateDeudaVenta(res["documento_contacto"], res["documento_sucursal"])

def updateDeudaVenta(documento, documento_sucursal):
    #=============== Obteniendo el total de todas las compras ===============#
    query = f"""SELECT * FROM venta WHERE documento_contacto = "{documento}";"""
    data_total = get_db_connection(query, op=True)
    deuda_total = calculateTotal(data_total)

    #=============== Actualizando la deuda del contacto con las compras que no hayan sido pago inmediato ===============#
    query = f"""UPDATE contacto SET deuda_contra = {deuda_total} WHERE documento = "{documento}";"""
    get_db_connection(query)

    #=============== Obteniendo el total de todas las ventas ===============#
    query = f"""SELECT * FROM venta WHERE documento_sucursal = "{documento_sucursal}";"""
    data_total_sucursal = get_db_connection(query, op=True)
    deuda_total_sucursal = calculateTotal(data_total_sucursal)

    #=============== Actualizando el total del contacto con las compras que no hayan sido pago inmediato ===============#
    query = f"""UPDATE contacto SET deuda_favor = {deuda_total_sucursal} WHERE documento = "{documento_sucursal}";"""
    get_db_connection(query)

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
    query = f"""SELECT cantidad FROM producto WHERE codigo = "{code}";"""
    data_cant = get_db_connection(query, op=False)
    
    if op:
        if data_cant[0] >= int(cant):
            query = f"""UPDATE producto SET cantidad = {data_cant[0]-int(cant)} WHERE codigo = "{code}";"""
            get_db_connection(query)
            return True
        return False
    else:
        query = f"""UPDATE producto SET cantidad = {data_cant[0]+int(cant)} WHERE codigo = "{code}";"""
        get_db_connection(query)

def deleteDeudaVenta(id):
    deuda_contra = 0

    #=============== Obteniendo el total de la venta ===============#
    query = f"SELECT * FROM venta WHERE id = {id};"
    data_total = get_db_connection(query, op=False)
    res = json_sale(data_total)

    #=============== Obteniendo la deuda_contra del contacto que realiza la compra ===============#
    query = f"""SELECT deuda_contra FROM contacto WHERE documento = "{res["documento_contacto"]}";"""
    data_deuda_contra = get_db_connection(query, op=False)

    deuda_contra = data_deuda_contra[0] - res["total"]
    
    query = f"""UPDATE contacto SET deuda_contra = {deuda_contra} WHERE documento = "{res["documento_contacto"]}";"""
    get_db_connection(query)

    #=============== Obteniendo la deuda_favor de la sucursal que realiza la venta ===============#
    query = f"""SELECT deuda_favor FROM contacto WHERE documento = "{res["documento_sucursal"]}";"""
    data_deuda_sucursal = get_db_connection(query, op=False)

    deuda_favor = data_deuda_sucursal[0] - res["total"]

    query = f"""UPDATE contacto SET deuda_favor = {deuda_favor} WHERE documento = "{res["documento_sucursal"]}";"""
    get_db_connection(query)

def updateAbono(cant_actual, cant_abono, deuda):
    if cant_actual > cant_abono:
        deuda = (cant_actual-cant_abono) + deuda
        return deuda

    deuda = (cant_abono-cant_actual) - deuda
    return deuda
