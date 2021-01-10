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
        db.sessin.commit()
        
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
        db.sessin.commit()
    
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
        db.sessin.commit()
    
    @staticmethod
    def get_all():
        return Platos.query.all()
db.create_all()