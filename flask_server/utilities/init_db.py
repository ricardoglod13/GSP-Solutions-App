import sqlite3

def create_db():
    with open('./utilities/schema.sql', 'r') as f:
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        data = f.read()
        cur.executescript(data)

    con.commit()
    con.close()
