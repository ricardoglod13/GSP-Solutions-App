from .db_queries import db_queries

def updateTotalCV(id, tabla):
    #=============== Obteniendo la venta donde se debe carcular el total ===============#
    res = db_queries('select', 'transaccion', where=['id'], where_value=[id], operators=['='], fields=['*'], fetch=0)
    total = 0
    for item in eval(res['items']):
        total += item['subtotal']

    #================ Actualizando el total de la venta ===============#
    db_queries('update', 'transaccion', where=['id'], where_value=[id], operators=['='],
        total=total
    )

    #================ Actualizando la deuda y credito de el cliente y la acreedor ===============#
    updateDeudaCV(f'{tabla}', res["deudor"], res["acreedor"])

def updateDeudaCV(tabla, documento_deudor, documento_acreedor):
    #=============== Obteniendo el total de todas las compras ===============#
    if tabla == 'venta':
        data_total = db_queries('select', 'transaccion', where=['deudor', 'tipo'], where_value=[documento_deudor, 'venta'], operators=['=', '='], fields=['*'], fetch=1)
    elif tabla == 'compra':
        data_total = db_queries('select', 'transaccion', where=['deudor', 'tipo'], where_value=[documento_deudor, 'compra'], operators=['=', '='], fields=['*'], fetch=1)
    deuda_total = calculateTotal(data_total)

    #=============== Actualizando la deuda del contacto con las compras que no hayan sido pago inmediato ===============#
    db_queries('update', 'contacto', where=['documento'], where_value=[documento_deudor], operators=['='],
        deuda= deuda_total
    )

    #=============== Obteniendo el total de todas las ventas ===============#
    if tabla == 'venta':
        data_total_acreedor = db_queries('select', 'transaccion', where=['acreedor', 'tipo'], where_value=[documento_acreedor, 'venta'], operators=['=', '='], fields=['*'], fetch=1)
    elif tabla == 'compra':
        data_total_acreedor = db_queries('select', 'transaccion', where=['acreedor', 'tipo'], where_value=[documento_acreedor, 'compra'], operators=['=', '='], fields=['*'], fetch=1)
    data_total_acreedor = calculateTotal(data_total_acreedor)

    #=============== Actualizando el total del contacto con las compras que no hayan sido pago inmediato ===============#
    db_queries('update', 'contacto', where=['documento'], where_value=[documento_acreedor], operators=['='],
        credito= data_total_acreedor
    )

def calculateTotal(data):
    deuda = []
    for dict in data:
        total = 0
        items = dict['items']
        plazo = dict['plazo']
        if items:
            products = eval(items)
            if plazo:
                for dic in products:
                    total = dic["subtotal"] + total
            deuda.append(total) 

    deuda_total = sum(deuda)

    return deuda_total

def updateInventory(code, cant, op):
    #=============== Obteniendo la cantidad del producto agregado ===============#
    data_cant = db_queries('select', 'producto', where=['codigo'], where_value=[code], operators=['='], fields=['cantidad'], fetch=0)
    
    if op:
        if data_cant['cantidad'] >= int(cant):
            db_queries('update', 'producto', where=['codigo'], where_value=[code], operators=['='],
                cantidad= data_cant['cantidad']-int(cant)
            )
            return True
        return False
    else:
        db_queries('update', 'producto', where=['codigo'], where_value=[code], operators=['='],
                cantidad= data_cant['cantidad']+int(cant)
            )

def deleteDeudaCV(id):

    #=============== Obteniendo el total de la venta ===============#
    res = db_queries('select', 'transaccion', where=['id'], where_value=[id], operators=['='], fields=['*'], fetch=0)

    #=============== Obteniendo la deuda del contacto que realiza la compra ===============#
    data_deuda = db_queries('select', 'contacto', where=['documento'], where_value=[res["deudor"]], operators=['='], fields=['deuda'], fetch=0)

    deuda_value = data_deuda['deuda'] - res["total"]

    db_queries('update', 'contacto', where=['documento'], where_value=[res["deudor"]], operators=['='], 
                deuda= deuda_value
            )

    #=============== Obteniendo la credito del acreedor que realiza la venta ===============#
    data_deuda_acreedor = db_queries('select', 'contacto', where=['documento'], where_value=[res["acreedor"]], operators=['='], fields=['credito'], fetch=0)

    credito_value = data_deuda_acreedor['credito'] - res["total"]

    db_queries('update', 'contacto', where=['documento'], where_value=[res["acreedor"]], operators=['='], 
                credito= credito_value
            )

def updateAbono(cant_actual, cant_abono, deuda):
    if cant_actual > cant_abono:
        deuda = (cant_actual-cant_abono) + deuda
        return deuda

    deuda = deuda - (cant_abono-cant_actual)
    return deuda
