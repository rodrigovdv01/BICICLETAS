
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    validators,
    IntegerField,
    Form,
)
from wtforms.validators import EqualTo

class LoginF(Form):
    username = StringField(
                'Username',
                [validators.DataRequired(message='Espacio requerido'),
                validators.length(min=5, max=30, message='No es valido')],
                render_kw={"placeholder":"user"}
                )
    password = PasswordField(
                'password',
                [validators.DataRequired(message='Espacio requerido'),
                validators.length(min=8, max=30, message='minimo 8 caracteres')],
                render_kw={"placeholder":"password"}
                )
    
    def __init__(self, *args, **kwargs):
        super(LoginF, self).__init__(*args, **kwargs)

class SignUpF(Form):
    username = StringField(
                'Username',
                [validators.DataRequired(message='Espacio requerido'),
                validators.length(min=5, max=30, message='No es valido')],
                render_kw={"placeholder":"username"}
                )       
    email = StringField(
                'Email',
                [validators.DataRequired(message='Debes colocar un correo')],
                render_kw={"placeholder":"email"}
                )
    password = PasswordField(
                'Password',
                [validators.DataRequired(message='Espacio requerido'),
                validators.length(min=8, max=30, message='minimo 8 caracteres')],
                render_kw={"placeholder":"password"}
                )
            

    def __init__(self, *args, **kwargs):
        super(SignUpF, self).__init__(*args, **kwargs)


class Bicicleta(Form):
    marca = StringField(
                'marca',
                [validators.DataRequired(message='Espacio requerido'),
                validators.length(min=1, max=30, message='No es valido')],
                render_kw={"placeholder":"Marca"}
                )       
    modelo = StringField(
                'modelo',
                [validators.DataRequired(message='Debes colocar un correo')],
                render_kw={"placeholder":"Modelo"}
                )
    aro = IntegerField(
                'aro',
                [validators.DataRequired(message='Espacio requerido')],
                render_kw={"placeholder":"Tamaño de aro"}
                )
    color = StringField(
                'color',
                [validators.DataRequired(message='Debes colocar un correo')],
                render_kw={"placeholder":"Color"}
                )
    tipo = StringField(
                'tipo',
                [validators.DataRequired(message='Debes colocar un correo')],
                render_kw={"placeholder":"Tipo"}
                )
    nivel = StringField(
                'nivel',
                [validators.DataRequired(message='Debes colocar un correo')],
                render_kw={"placeholder":"Nivel"}
                )
    precio = IntegerField(
                'precio',
                [validators.DataRequired(message='Espacio requerido')],
                render_kw={"placeholder":"Precio"}
                )
    imagen = StringField(
                'imagen',
                render_kw={"placeholder":"image URL"}
                )
    def __init__(self, *args, **kwargs):
        super(Bicicleta, self).__init__(*args, **kwargs)