from flask_mysqldb import MySQL

db = MySQL()

class actions:
    def mostrar(self,query):
        cursor = db.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    def guardar(self,query):
        cursor = db.connection.cursor()
        cursor.execute(query)
        db.connection.commit()

def close_connection():
    cursor = db.connection.cursor()
    return cursor.close()