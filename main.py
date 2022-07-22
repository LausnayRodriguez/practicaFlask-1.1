
from datetime import timedelta
from flask import Flask, render_template, url_for, redirect, request, g, session
from flask_mysqldb import MySQL
from backend.database import actions, close_connection

app = Flask(__name__) 

app.config['MYSQL_HOST'] = 'mysql.perseoq.party'
app.config['MYSQL_USER'] = 'superanet'
app.config['MYSQL_PASSWORD'] = 'the37855'
app.config['MYSQL_DB'] = 'mydb'
app.secret_key = 'mi_llave'

MySQL(app) # conexión a la base de datos
my = actions() # constructor del mini ORM (database.py)

from datetime import timedelta
@app.before_request
def antes_de():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)
    g.user = None
    if 'user' in session:
        g.user = session['user']
    
@app.teardown_appcontext
def shutdown_session(exception=None):
    close_connection()

@app.route('/')
def principal():
    return render_template('home/index.html')

@app.route('/', methods=['GET', 'POST'])
def entrar():
    if request.method=='POST':
        session.pop('user', None)
        if request.method=='POST':
            username = request.form['usuario']
            passwd = request.form['clave']
            query = f'SELECT * FROM users WHERE user="{username}" AND passw="{passwd}" '
            datos = my.mostrar(query)
            if datos:
                session['user'] = request.form['usuario']
                return redirect(url_for('index'))
            return redirect(url_for('principal'))
        return redirect(url_for('principal'))
    return render_template('home/index.html')

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('user', None)
    return redirect(url_for('principal'))

@app.route('/home')
def index():
    if g.user:
        query = 'SELECT * FROM users'
        # fetch es para mostrar
        datos = my.mostrar(query)
        return render_template('home/principal.html', datos_mostrar=datos, user=session['user'])
    return redirect(url_for('principal'))

@app.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if g.user:
        if request.method == 'POST':
            usuario = request.form['user_form']
            clave = request.form['pw_form']
            query = f"INSERT INTO users(user,passw) VALUES('{usuario}','{clave}')"
            # commit es para enviar
            my.guardar(query)
            return redirect(url_for('index', user=session['user']))
        return redirect(url_for('index'))
    return redirect(url_for('principal'))

@app.route('/borrar/<string:id>')
def borrar_dato(id):
    if g.user:
        query= f'DELETE FROM users WHERE id={id}'
        my.guardar(query)
        return redirect(url_for('index', user=session['user']))
    return redirect(url_for('principal'))

@app.route('/actualiza/<string:id>')
def obtener_datos(id):
    if g.user:
        query = f'SELECT * FROM users WHERE id={id}'
        datos = my.mostrar(query)
        return render_template('home/obtener.html', datos=datos[0], user=session['user'])
    return redirect(url_for('principal'))


@app.route('/actualizar/<string:id>', methods=['GET', 'POST'])
def update(id):
    if g.user:
        if request.method == 'POST':
            usuario = request.form['user_form']
            clave = request.form['pw_form']
            # SET es poner el valor en el campo SQL
            query = f"UPDATE users SET user='{usuario}', passw='{clave}' WHERE id='{id}' "
            my.guardar(query)
            return redirect(url_for('index', user=session['user']))
        return redirect(url_for('index'))
    return redirect(url_for('principal'))


if __name__=='__main__':
    app.run(debug=True)