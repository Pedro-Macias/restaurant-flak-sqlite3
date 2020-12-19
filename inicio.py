from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
import sqlite3

app = Flask(__name__)


''''
CREAMOS LA FUNCION  para crear base de datos y tablas
'''
def crear_base():
    # crear base de datos o conectarse si esta creada
    conexion = sqlite3.connect('database/chiringuito.db')
    # crear cursor de la base de datos
    cursor = conexion.cursor()
    try:
        # creamos la 1 tabla
        cursor.execute("CREATE TABLE opciones (id INTEGER PRIMARY KEY AUTOINCREMENT, opcion VARCHAR(100) UNIQUE NOT NULL)")
    except sqlite3.OperationalError:
        print(' la tabla de opciones ya existe')
    else:
        print('tabla de Opciones creada correctamente')
    
    try:
        # creamos la segunda tabla
        cursor.execute("CREATE TABLE platos(id INTEGER PRIMARY KEY AUTOINCREMENT, plato VARCHAR(100) UNIQUE NOT NULL,precio FLOAT ,categoria_id INTEGER NOT NULL FOREIGN KEY(categoria_id) REFERENCES categoria(id))")
    except sqlite3.OperationalError:
        print('la tabla Platos ya existe')
    else:
        print('tabla Platos creada correctamente')
    
    conexion.close()
# crear base de datos
crear_base()
# INICIAR  una session 
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    #conectamos con la base de datos . con el cursor
    conexion = sqlite3.connect('database/chiringuito.db')
    cursor =conexion.cursor()
    # le damos la orden , lo que queremos obtener
    cursor.execute('SELECT * FROM opciones')
    #ejecutamos la orden y obtenemos los datos , almacenandolos en una variable
    datos = cursor.fetchall()
    conexion.close()
    return render_template('index.html', opciones = datos)


# Crear categoria
@app.route('/add_opcion',methods=['POST'])
def add_opcion():
    if request.method == 'POST':
        opcion=request.form['opcion']
        conexion = sqlite3.connect('database/chiringuito.db')
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO opciones VALUES (null,'{}')".format(opcion))
            conexion.commit()
        except sqlite3.IntegrityError:
            flash('esa Opcion ya existe')
            return redirect(url_for('index'))
        else:
            flash('Categoria Creada Correctamente')
            # lo redireccionarmos a la pagina principal una vez enviado el dato
            return redirect(url_for('index'))
    
    conexion.close()

# borrar categoria
@app.route('/borrar_opcion/<id>')
def borrar_opcion(id):
    # nos conectamos a MYSQL
    conexion = sqlite3.connect('database/chiringuito.db')
    cursor = conexion.cursor()
    # ejecutamos la orden , que borre de la tabla la linea con el id que indicamos
    cursor.execute('DELETE FROM opciones WHERE id = {0}'.format(id))
    # enviamos a la base de datos para ejecutar
    conexion.commit()
    # enviamos un mensaje
    flash('Contacto Eliminado Correctamente ')
    #redireccionamos a la pagina
    conexion.close()
    return redirect(url_for('index'))
    




# ir a pagina platos

# def mostrar_platos(id):
#     conexion = sqlite3.connect('database/chiringuito.db')
#     cursor = conexion.cursor()
    
#     conexion.close()

@app.route('/get_platos/<id>')
def get_platos(id):

    # nos conectamos a MYSQL
    conexion = sqlite3.connect('database/chiringuito.db')
    cursor = conexion.cursor()
    # conectamos con la base de datos
    cursor.execute('SELECT * FROM opciones WHERE id = {}'.format(id))
    # escribimos la consulta que queremos 
    opciones = cursor.fetchall()
    conexion.close()

    conexion = sqlite3.connect('database/chiringuito.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM platos WHERE categoria_id ={}'.format(id))
    platos = cursor.fetchall()
    # ejecuctamos la consulta , recibiendo la tupla
    conexion.close()
    return render_template('get_platos.html',opciones = opciones[0],platos=platos)
    



@app.route('/add_platos/<id>',methods=['POST'])
def add_platos(id):
    if request.method == 'POST':
        plato=request.form['plato']
        precio=request.form['precio']
        conexion = sqlite3.connect('database/chiringuito.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM opciones WHERE id = {}'.format(id))
        opciones = cursor.fetchall()
        try:
            cursor.execute("INSERT INTO platos VALUES (null,'{}','{}','{}')".format(plato,precio,id))
            conexion.commit()
        except sqlite3.IntegrityError:
            flash('ese tipo ya existe')
            return get_platos(id)
        else:
            tipo=(opciones[0])
            flash('{} Creada Correctamente'.format(tipo[1]))
            # lo redireccionarmos a la pagina principal una vez enviado el dato
            return get_platos(id)
    
    conexion.close()

@app.route('/borrar_plato/<id>')
def borrar_plato(id):
    conexion = sqlite3.connect('database/chiringuito.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT categoria_id FROM platos WHERE id ={0}'.format(id))
    id_platos = cursor.fetchall()
    id_p = id_platos[0]
    platos = id_p[0]
    print(id_p)

    conexion.close()
    
    # return redirect(url_for('index'))
    
    conexion = sqlite3.connect('database/chiringuito.db')
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM platos WHERE id = {0}".format(id))
    conexion.commit()
    flash('Plato borrado Correctamente')
    conexion.close()
    return get_platos(platos)
    
@app.route('/ver_menu')
def ver_menu():
    conexion = sqlite3.connect('database/chiringuito.db')
    cursor = conexion.cursor()
    # consultar categorias
    opciones = cursor.execute("SELECT * FROM opciones").fetchall()

    conexion.close()
    conexion = sqlite3.connect('database/chiringuito.db')
    cursor = conexion.cursor()
    platos = cursor.execute("SELECT * FROM platos").fetchall()

    return render_template('ver_menu.html', opciones = opciones, platos=platos)


# # crear base de datos




if __name__ == '__main__':
    app.run(port = 8000, debug = True)
    # http://localhost:8000
