from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FloatField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class Form_Registro(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class Form_Categoria(FlaskForm):
    opcion =StringField('Opcion', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Enviar')

class Form_Platos(FlaskForm):
    plato =StringField('Plato', validators=[DataRequired(), Length(max=50)])
    precio =FloatField('Precio', validators=[DataRequired()])
    submit = SubmitField('Enviar') 

class Form_login(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')