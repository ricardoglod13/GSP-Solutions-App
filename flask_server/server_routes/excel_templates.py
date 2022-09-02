from flask import send_file
import pandas as pd
import shutil
from utilities.db_queries import db_queries
from utilities.functions import *
from __init__ import flask_routes

#=============== Product Template ===============#

@flask_routes.route('/products/template', methods=['GET'])
def productTemplate():

    data = {
            'codigo':[],
            'tipo':[],
            'descripcion':[],
            'precio_costo':[],
            'precio_venta':[],
            'cantidad':[]
        }
    
    data = pd.DataFrame(data)
    data.to_excel('productsTemplate.xlsx', sheet_name='Productos', engine='openpyxl')
    shutil.move('productsTemplate.xlsx', 'excel_templates/productsTemplate.xlsx')
    return send_file('excel_templates\productsTemplate.xlsx', as_attachment=True)

#=============== Contact Template ===============#

@flask_routes.route('/contacts/template', methods=['GET'])
def contactTemplate():

    data = {
            'documento':[],
            'nombre':[],
            'telefono':[],
            'direccion':[],
            'credito': [],
            'deuda':[],
            'tipo':[]
        }
    
    data = pd.DataFrame(data)
    data.to_excel('contactsTemplate.xlsx', sheet_name='Contactos', engine='openpyxl')
    shutil.move('contactsTemplate.xlsx', 'excel_templates/contactsTemplate.xlsx')
    return send_file('excel_templates\contactsTemplate.xlsx', as_attachment=True)

#=============== Transaction Template ===============#

@flask_routes.route('/transactions/template', methods=['GET'])
def transactionTemplate():

    data = {
            'acreedor':[],
            'deudor':[],
            'items':[],
            'plazo':[],
            'cantidad_pagada': [],
            'total':[],
            'tipo':[],
            'fecha':[]
        }
    
    data = pd.DataFrame(data)
    data.to_excel('contactsTemplate.xlsx', sheet_name='Contactos', engine='openpyxl')
    shutil.move('contactsTemplate.xlsx', 'excel_templates/contactsTemplate.xlsx')
    return send_file('excel_templates\contactsTemplate.xlsx', as_attachment=True)