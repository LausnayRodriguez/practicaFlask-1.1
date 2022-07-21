from flask_mysqldb import MySQL

db = MySQL()

class actions:

    def fetchall(query):
        cursor= db.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    def commit(query):
        cursor = db.connection.cursor()
        cursor.execute(query)
        db.connection.commit()