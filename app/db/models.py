from flask import Flask, jsonify, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from .database import db

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    email = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password_hashed = db.Column(db.String(), nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hashed = password

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    def check_password(self, password):
        return self.password_hashed == password
    
    def get_id(self):
        return (self.email)
    
    def __repr__(self) -> str:
        return f'{self.username}'

class Bicicleta(db.Model):
    __tablename__ = 'bicicleta'
    id = db.Column(db.Integer(), primary_key = True)
    marca = db.Column(db.String(), nullable = False)
    modelo = db.Column(db.String(), nullable = False)
    aro = db.Column(db.Integer(), nullable = False)
    color = db.Column(db.String(), nullable = False)
    tipo = db.Column(db.String(), nullable = False)
    nivel = db.Column(db.String(), nullable = False)
    precio = db.Column(db.Integer(), nullable = False)
    imagen = db.Column(db.String(), nullable = False)
    id_usuario = db.Column(db.String(50), db.ForeignKey('usuario.email'), nullable=True)

    usuario = db.relationship("Usuario", backref="personas")
    def __repr__(self):
        response = {}
        response['marca'] = self.marca
        response['usuario'] = self.id_usuario
        response['modelo'] = self.modelo
        response['aro'] = self.aro
        response['color'] = self.color
        response['tipo'] = self.tipo
        response['precio'] = self.precio
        response['imagen'] = self.imagen