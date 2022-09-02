import sqlite3

def create_db():
    with open('./utilities/schema.sql', 'r') as f:
        con = sqlite3.connect('database.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        data = f.read()
        cur.executescript(data)

    con.commit()
    con.close()

def get_db_connection(query, **kwargs):
    print(query)

    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f'{query}') 
    con.commit()
    if query[0:6] != "SELECT":
        con.close()
    elif kwargs.get('op'):
        data = cur.fetchall()
        data = [dict(row) for row in data]
        con.close()
        return (data)
    elif not kwargs.get('op'):
        data = cur.fetchone()
        data = dict(data)
        con.close()
        return (data)
