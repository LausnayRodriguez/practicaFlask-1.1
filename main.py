

from flask import Flask, render_template, url_for, redirect, request
from flask_mysqldb import MySQL
from backend.database import actions


app = Flask(__name__)

app.config["MYSQL_HOST"] = "mysql.perseoq.party"
app.config["MYSQL_USER"] = "superanet"
app.config["MYSQL_PASSWORD"] = "the37855"
app.config["MYSQL_DB"] = "mydb"
app.secret_key = "mi_llave" # Llave secreta para modificar el codigo (debugger)

MySQL(app) #c conexion a la base de datos
my = actions # constructor del mini ORM (database.py)

@app.route('/')
def index():
    query = "SELECT * FROM users"
    datos = my.fetchall(query) #fetchall es para mostrar datos
    return render_template("home/principal.html", datos_mostrar=datos)

@app.route('/insertar', methods=["GET", "POST"])
def insertar():
    if request.method == "POST":
        usuario = request.form["user_form"]
        clave = request.form["pw_form"]
        query = f"INSERT INTO users(user,passw) VALUES('{usuario}', '{clave}')"
        my.commit(query) # commit es para enviar 
        return redirect(url_for("index"))

    return redirect(url_for("index"))

@app.route('/borrar/<string:id>')
def borrar_dato(id):
    cursor = db.connection.cursor()
    cursor.execute(f'DELETE FROM users WHERE id={id}')
    db.connection.commit()
    return redirect(url_for('index'))



@app.route('/actualiza/<string:id>')
def obtener_datos(id):
    cursor = db.connection.cursor()
    cursor.execute(f'SELECT * FROM users WHERE id={id}')
    datos = cursor.fetchall()
    return render_template('home/obtener.html', datos=datos[0])

@app.route('/actualizar/<string:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == "POST":
        usuario = request.form["user_form"]
        clave = request.form["pw_form"]
        cursor = db.connection.cursor()
        cursor.execute(f"UPDATE users SET user='{usuario}', passw='{clave}' WHERE id='{id}'")
        db.connection.commit()
        return redirect(url_for("index"))

    return redirect(url_for("index"))




if __name__=="__main__":
    app.run(debug=True)