from flask import send_file
import pandas as pd
import shutil
from utilities.db_queries import db_queries
from utilities.functions import *
from __init__ import flask_routes

#=============== Product Template ===============#

@flask_routes.route('/products/template', methods=['GET'])
def productTemplate():
    data_query = db_queries('select', 'producto', fields=['*'])
    products = json_product(data_query)

    data = {
            'codigo':[],
            'tipo':[],
            'descripcion':[],
            'precio_costo':[],
            'precio_venta':[],
            'cantidad':[]
        }
    if products:
        for dict in products:
            for key in dict:
                if key != 'id':
                    data[key].append(dict[key])
    
    data = pd.DataFrame(data)
    data.to_excel('productsTemplate.xlsx', sheet_name='Productos', engine='openpyxl')
    shutil.move('productsTemplate.xlsx', 'excel_templates/productsTemplate.xlsx')
    return send_file('excel_templates\productsTemplate.xlsx', as_attachment=True)

#=============== Contact Template ===============#

@flask_routes.route('/contacts/template', methods=['GET'])
def contactTemplate():
    data_query = db_queries('select', 'contacto', fields=['*'])
    contacts = json_contact(data_query)

    data = {
            'documento':[],
            'nombre':[],
            'telefono':[],
            'direccion':[],
            'tipo':[]
        }
    if contacts:
        for dict in contacts:
            for key in dict:
                if key != 'id' and key != 'deuda_contra' and key != 'deuda_favor':
                    data[key].append(dict[key])
    
    data = pd.DataFrame(data)
    data.to_excel('contactsTemplate.xlsx', sheet_name='Contactos', engine='openpyxl')
    shutil.move('contactsTemplate.xlsx', 'excel_templates/contactsTemplate.xlsx')
    return send_file('excel_templates\contactsTemplate.xlsx', as_attachment=True)