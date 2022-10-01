from flask import Blueprint, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField,
    StringField,
    PasswordField,
    validators,
    IntegerField,
    FileField,
    Form,
    SubmitField
)

class LoginF(Form):
    username = StringField(
                'Username',
                [validators.DataRequired(message='Espacio requerido'),
                validators.length(min=5, max=30, message='No es valido')]
                )
    password = PasswordField(
                'Password',
                [validators.DataRequired(message='Espacio requerido'),
                validators.length(min=8, max=30, message='minimo 8 caracteres')]
                )
    
    def __init__(self, *args, **kwargs):
        super(LoginF, self).__init__(*args, **kwargs)

class SignUpF(Form):
    username = StringField(
                'Username',
                [validators.DataRequired(message='Espacio requerido'),
                validators.length(min=5, max=30, message='No es valido')]
                )       
    email = StringField(
                'Email',
                [validators.DataRequired(message='Debes colocar un correo')]
                )
    password = PasswordField(
                'Password',
                [validators.DataRequired(message='Espacio requerido'),
                validators.length(min=8, max=30, message='minimo 8 caracteres')]
                )
    
    def __init__(self, *args, **kwargs):
        super(SignUpF, self).__init__(*args, **kwargs)

class LoginF(Form):
    username = StringField(
                'Username',
                [validators.DataRequired(message='Espacio requerido'),
                validators.length(min=5, max=30, message='No es valido')]
                )
    password = PasswordField(
                'Password',
                [validators.DataRequired(message='Espacio requerido'),
                validators.length(min=8, max=30, message='minimo 8 caracteres')]
                )
    
    def __init__(self, *args, **kwargs):
        super(LoginF, self).__init__(*args, **kwargs)

class Bicicleta(Form):
    marca = StringField(
                'marca',
                [validators.DataRequired(message='Espacio requerido'),
                validators.length(min=1, max=30, message='No es valido')]
                )       
    modelo = StringField(
                'modelo',
                [validators.DataRequired(message='Debes colocar un correo')]
                )
    aro = IntegerField(
                'aro',
                [validators.DataRequired(message='Espacio requerido')]
                )
    color = StringField(
                'color',
                [validators.DataRequired(message='Debes colocar un correo')]
                )
    tipo = StringField(
                'tipo',
                [validators.DataRequired(message='Debes colocar un correo')]
                )
    nivel = StringField(
                'nivel',
                [validators.DataRequired(message='Debes colocar un correo')]
                )
    precio = IntegerField(
                'precio',
                [validators.DataRequired(message='Espacio requerido')]
                )
    def __init__(self, *args, **kwargs):
        super(Bicicleta, self).__init__(*args, **kwargs)