from django.shortcuts import render
from flask import (
    Blueprint,
    Flask,
    flash,
    abort,
    jsonify,
    render_template,
    redirect,
    session,
    url_for,
    request
)
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    current_user
)

import hashlib
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from .db.database import db

from . import forms
from .db.models import Usuario, Bicicleta
from werkzeug.utils import secure_filename

app = Blueprint('login', __name__,
                template_folder='templates')

def init_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_email):
        return Usuario.query.get(user_email)

@app.route('/', methods=['GET'])
def index():
    return render_template('Inicio.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.route('/sign-up/', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpF(request.form)
    if request.method == 'POST':
        email = form.email.data
        username = form.username.data
        password = form.password.data
        usuario = Usuario(email, username, password) 

        email_const = Usuario.query.filter_by(email=email).first()
        user_const = Usuario.query.filter_by(username=username).first()

        if (email_const is not None):
            if (email == email_const.email):
                return render_template('signup.html', form=form) 
        if (user_const is not None):
            if  (username == user_const.username):
                return render_template('signup.html', form=form)  

        db.session.add(usuario)
        db.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("login.inicio"))
    elif request.method == 'GET':
        return render_template("signup.html", form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = forms.LoginF(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data

        usuario = Usuario.query.filter_by(username = username).first()
        if (usuario is not None and usuario.check_password(password)):
            login_user(usuario, remember=True)
            return redirect(url_for("login.inicio"))
        return render_template('login.html', form=form)
    else:
        return render_template('login.html', form = form)

@app.route('/inicio', methods=['GET', 'POST'])
@login_required
def inicio():
    form = forms.Bicicleta(request.form)
    if request.method == 'POST':
        bicicleta = Bicicleta(
            marca = form.marca.data,
            modelo = form.modelo.data,
            aro = form.aro.data,
            color = form.color.data,
            tipo = form.tipo.data,
            nivel = form.nivel.data,
            precio = form.precio.data,
            id_vendedor = current_user.email
        )
        db.session.add(bicicleta)
        db.session.commit()
        subquery = db.session.query(Bicicleta.id).filter(Bicicleta.id_vendedor == current_user.email).scalar_subquery()
        p = Bicicleta.query.filter(Bicicleta.id.in_(subquery)).all()

        if p is not None:
            return redirect('inicio')
    subquery = db.session.query(Bicicleta.id).filter(Bicicleta.id_vendedor == current_user.email).scalar_subquery()
    p = Bicicleta.query.filter(Bicicleta.id.in_(subquery)).all()        
    return render_template('Index.html', form = form, bicicletas = p)

@app.route('/show-data/<user>', methods=['GET'])
@login_required
def agregar(user):
    response = {}
    id = int(user)
    bicicleta = Bicicleta.query.get(id)
    response['Marca'] = bicicleta.marca
    response['Modelo'] = bicicleta.modelo
    response['Aro'] = bicicleta.aro
    response['Color'] = bicicleta.color
    response['Tipo'] = bicicleta.tipo
    response['Nivel'] = bicicleta.nivel
    response['Precio'] = bicicleta.precio
    response['user'] = bicicleta.id_vendedor

    return jsonify(response)

@app.route('/actualizar/<id>', methods=['GET','POST'])
@login_required
def actualizar(id):
    form = forms.Bicicleta(request.form)
    if request.method == 'POST':
        bicicleta = Bicicleta.query.filter(Bicicleta.id == id).one_or_none()
        bicicleta.marca = form.marca.data
        bicicleta.modelo = form.modelo.data
        bicicleta.aro = int(form.aro.data)
        bicicleta.color = form.color.data
        bicicleta.tipo = form.tipo.data
        bicicleta.nivel = form.nivel.data
        bicicleta.precio = int(form.precio.data)
        db.session.commit()
        return redirect(url_for("login.inicio"))
    return render_template('actualizar.html', form = form, id=id)

@app.route('/delete/<id>', methods=['GET','DELETE'])
@login_required
def eliminar(id):
    response = {}
    try:
        bicicleta = Bicicleta.query.get(id) # 1 registro
        db.session.delete(bicicleta)
        response['id'] = bicicleta.id
        db.session.commit()
        return jsonify(response)
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
        return jsonify(response)