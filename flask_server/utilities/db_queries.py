from .functions import *

def db_queries(action, table, **kwargs):
    if action == 'select'and not kwargs.get("where"):
        query = f"""{action.upper()} * FROM {table};"""
        data = get_db_connection(query, op=True)
        return data

    elif action == 'select' and kwargs.get("where") and not kwargs.get("fields"):
        where_value = multi_kwargs(action, kwargs)
        query = f"""{action.upper()} * FROM {table} WHERE {kwargs.get("where")} = {where_value};"""
        data = get_db_connection(query, op=False)
        return data

    elif action == 'select' and kwargs.get("where") and kwargs.get("fields"):
        arguments = multi_kwargs(action, kwargs)
        print(arguments)
        query = f"""{action.upper()} {arguments["fields"]} FROM {table} WHERE {kwargs.get("where")} = {arguments["where_value"]};"""
        data = get_db_connection(query, op=False)
        return data

    elif action == 'delete':
        query = f"""{action.upper()} FROM {table} WHERE {kwargs.get("where")} = {kwargs.get("where_value")};"""
        get_db_connection(query)

    elif action == 'update':
        arguments = multi_kwargs(action, kwargs)
        query = f"""{action.upper()} {table} SET {arguments["data"]} WHERE {kwargs.get("where")} = {arguments["where_value"]};"""
        get_db_connection(query)
            
    elif action == 'insert':
        data = multi_kwargs(action, kwargs)
        query = f"""{action.upper()} INTO {table} ({data[0]}) VALUES ({data[1]});"""
        get_db_connection(query)

def multi_kwargs(action, kwargs):
    i = 0

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
            if isNotNan:
                where_value = f"""{kwargs["where_value"]}"""
            else:
                where_value = f""""{kwargs["where_value"]}" """
            i += 1
        return {'data': data, 'where_value': where_value}
    
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
    
    elif action == 'select':
        fields = ""
        print(kwargs)
        if 'fields' in kwargs:
            if isNumeric(str(kwargs["where_value"])):
                for field in kwargs["fields"]:
                    fields += field
                where_value = f"""{kwargs["where_value"]}"""
                return {'fields': fields, 'where_value': where_value}
            else:
                for field in kwargs["fields"]:
                    fields += field
                where_value = f"""'{kwargs["where_value"]}'"""
                return {'fields': fields, 'where_value': where_value}
        else:
            if isNumeric(str(kwargs["where_value"])):
                where_value = f"""{kwargs["where_value"]}"""
                return where_value
            else:
                where_value = f"""'{kwargs["where_value"]}'"""
                return where_value
         
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
