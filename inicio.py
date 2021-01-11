""" Proyecto Mi Bar , Pedro Macias , 2021 """

#  para empezar el entrno virtual , env\Scripts\activate.bat , para pararlo:  deactivate

from flask import Flask
from flask import render_template, request, redirect, url_for
from flask import flash
from formularios import Form_Registro, Form_login, Form_Categoria, Form_Platos
from flask_login import LoginManager
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import sqlite3

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mi-clave-secreta'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///bar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)



from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Boolean, Column , ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
# from inicio import db

class User(db.Model, UserMixin):
    __tablename__ = 'blog_user'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<User{self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password (self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

class Categoria(db.Model, UserMixin):
    __tablename__= "categoria"
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='CASCADE'),nullable=False)
    opcion = db.Column(db.String(80), nullable=False, unique=True)

    def __repr__(self):
        return f'<Categoria {self.opcion}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return Categoria.query.all()

class Platos(db.Model, UserMixin):
    __tablename__= "platos"
    id = db.Column(db.Integer, primary_key= True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'),nullable=False)
    plato = db.Column(db.String(80),nullable = False, unique=True)
    precio = db.Column(Float,default=0)

    def __repr__(self):
        return f'<Platos {self.plato}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return Platos.query.all()

db.create_all()



platos = []

@app.route('/')
def index():
    ''' funcion pagina principal'''
    categorias = Categoria.get_all()
    return render_template ('index.html',categorias=categorias, platos=platos)
    

@app.route('/p/<string:slug>/')
def ver_menu(slug):
    return render_template('ver_menu.html',slug_nombre = slug)

@app.route('/add_carta')
def ver_carta():
    categorias = Categoria.get_all()
    return render_template ('add_carta.html',categorias=categorias, platos=platos)


@app.route("/admin/categoria/", methods=['GET','POST'],defaults={'categoria_id' : None})
@app.route("/admin/categoria/<int:categoria_id>/", methods= ['GET','POST'])
@login_required
def form_cat(categoria_id):
    form = Form_Categoria()
    if form.validate_on_submit():
        
        try:
            opcion = form.opcion.data
            categoria = Categoria(user_id=current_user.id, opcion=opcion)          
            categoria.save()
            
        except exc.SQLAlchemyError:
            flash('esa Opcion ya existe')
            return redirect(url_for('form_cat'))
        else:
            flash('Categoria creada correctamente')
            return redirect(url_for('ver_carta'))


    return render_template('admin/form_cat.html', form=form)


@app.route("/registro/", methods=['GET','POST'])
def show_form_registro():
    '''funcion registro de ususarios'''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Form_Registro()
    error = None
    if form.validate_on_submit():
        ''' validate_on_submit(). Este método comprueba por nosotros 
        que se ha enviado el formulario y que todos sus campos son válidos.'''
        nombre = form.nombre.data
        email = form.email.data
        password = form.password.data

        user = User.get_by_email(email)
        if user is not None:
            flash('esa email {email} ya esta siendo utilizado')
        else:
            user = User(nombre = nombre, email=email)
            user.set_password(password)
            user.save()
            login_user(user, remember=True)

            '''Comprobamos si se pasó por la URL el parámetro next.
            Este parámetro lo usaremos para redirigir al usuario
            a la página que se indica ''' 
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)    
    return render_template("form_registro.html", form=form, error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Form_login()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    flash('usuario incorrecto')        
    return render_template('form_login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route("/admin/plato/", methods=['GET','POST'],defaults={'plato_id' : None})
@app.route("/admin/plato/<int:plato_id>/", methods= ['GET','POST'])
def form_platos(plato_id):
    form = Form_Platos()
    if form.validate_on_submit():
        nombre = form.nombre.data
        precio = form.precio.data 
        plato ={'nombre': nombre , 'precio': precio}
        platos.append(plato)
        return redirect(url_for('index'))
    if form.validate_on_submit():
        nombre = form.nombre.data
        precio = form.precio.data 
        plato ={'nombre': nombre , 'precio':precio}
        platos.append(plato)
        return redirect(url_for('ver_carta'))
    return render_template('admin/get_platos.html', form=form)

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
    


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))