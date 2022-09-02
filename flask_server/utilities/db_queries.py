from .init_db import *

def db_queries(action, table, **kwargs):

    #=============== Resolviendo SELECT sin condicion ===============#
    if action == 'select'and not kwargs.get("where"):
        fields = multi_kwargs(action, kwargs)
        query = f"""{action.upper()} {fields} FROM {table};"""
        data = get_db_connection(query, op=True)
        return data

     #=============== Resolviendo SELECT con condicion ===============#
    elif action == 'select' and kwargs.get("where"):
        arguments = multi_kwargs(action, kwargs)
        query = f"""{action.upper()} {arguments["fields"]} FROM {table} WHERE {kwargs.get("where")} = {arguments["where_value"]};"""
        if kwargs.get("fetch"):
            data = get_db_connection(query, op=True)
        else:
            data = get_db_connection(query, op=False)
        return data

     #=============== Resolviendo DELETE ===============#
    elif action == 'delete':
        query = f"""{action.upper()} FROM {table} WHERE {kwargs.get("where")} = {kwargs.get("where_value")};"""
        get_db_connection(query)

     #=============== Resolviendo UPDATE ===============#
    elif action == 'update':
        arguments = multi_kwargs(action, kwargs)
        query = f"""{action.upper()} {table} SET {arguments["data"]} WHERE {kwargs.get("where")} = {arguments["where_value"]};"""
        get_db_connection(query)

     #=============== Resolviendo INSERT ===============#            
    elif action == 'insert':
        data = multi_kwargs(action, kwargs)
        query = f"""{action.upper()} INTO {table} ({data[0]}) VALUES ({data[1]});"""
        get_db_connection(query)

def multi_kwargs(action, kwargs):
    i = 0

    #=============== Formateando argumentos obtenidos UPDATE ===============#
    if action == 'update':
        data = ""
        for key in kwargs:
            isNotNan = isNumeric(str(kwargs[key]))
            if key != 'where' and key != 'where_value':
                if i < len(kwargs) - 3:
                    if not isNotNan and kwargs[key] != 0 and kwargs[key] != 1:
                        data += f"""{key} = "{kwargs[key]}", """
                    else:
                        data += f"""{key} = {kwargs[key]}, """
                    
                else:
                    if not isNotNan and kwargs[key] != 0 and kwargs[key] != 1: 
                        data += f"""{key} = "{kwargs[key]}" """
                    else:
                        data += f"""{key} = {kwargs[key]}"""
                i += 1
            if key == 'where_value':
                if isNotNan:
                    where_value = f"""{kwargs["where_value"]}"""
                else:
                    where_value = f""""{kwargs["where_value"]}" """
        return {'data': data, 'where_value': where_value}
    
    #=============== Formateando argumentos obtenidos INSERT ===============#
    elif action == 'insert':
        campos = ""
        valores = ""
        for key in kwargs:
            isNotNan = isNumeric(str(kwargs[key]))
            if i < len(kwargs) - 1:
                campos += f"""{key}, """
                if not isNotNan and kwargs[key] != 0 and kwargs[key] != 1: 
                    valores += f""""{kwargs[key]}", """
                else:
                    valores += f"""{kwargs[key]}, """
            else:
                campos += f"""{key}"""
                if not isNotNan and kwargs[key] != 0 and kwargs[key] != 1: 
                    valores += f""""{kwargs[key]}" """
                else:
                    valores += f"""{kwargs[key]}"""
            i += 1
        return campos, valores
    
    #=============== Formateando argumentos obtenidos SELECT ===============#
    elif action == 'select':
        fields = ""
        if 'fields' in kwargs:
            for field in kwargs["fields"]:
                if kwargs['fields'].index(field) < (len(kwargs['fields']) -1):
                    fields += field + ","
                else:
                    fields += field
            if "where" in kwargs and "where_value" in kwargs:
                for key in kwargs:
                    if key == "where_value":
                        if isNumeric(str(kwargs["where_value"])):
                            where_value = f"""{kwargs["where_value"]}"""
                            return {'fields': fields, 'where_value': where_value}
                        else:
                            where_value = f""""{kwargs["where_value"]}" """
                            return {'fields': fields, 'where_value': where_value}
            return fields
         
def isNumeric(valor):
    if valor.find("."):
        try:
            float(valor)
            return True
        except ValueError:
            return False
    else:
        try:
            int(valor)
            return True
        except ValueError:
            return False
