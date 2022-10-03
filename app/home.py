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
    logout_user,
    login_required,
    current_user
)

import bcrypt
import hashlib
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from .db.database import db
from . import forms
from .db.models import Usuario, Bicicleta
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Blueprint('login', __name__,
                template_folder='templates')

#Sirve para loggear al usuario
def init_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_email):
        return Usuario.query.get(user_email)


#Route - página principal. Se muestra el template Inicio.html
#la variable bicicletas hace una consulta a la base de datos sobre las bicicletas que se han registrado
@app.route('/', methods=['GET'])
def index():
    bicicletas = Bicicleta.query.all()
    return render_template('Inicio.html', bicicletas = bicicletas)
# Error handler por si no se encuentra la página
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


#READ
#Controller - mostrar datos de la bicicleta
#Consulta el id y retorna un objeto json
#para mostrar los datos de la bicicleta seleccionada y el usuario que la publicó
@app.route('/show-data/<user>', methods=['GET'])
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
    response['Imagen'] = bicicleta.imagen
    response['user'] = bicicleta.id_usuario

    return jsonify(response)

#CREATE USER
#Segunda ruta - sign-up. Se muestra el template signup.html
#Asignamos el formulario que se va a mostrar en la página SignUpF
#Si el método es post, asigna los datos ingresados en el formulario a un nuevo usuario al hacer submit.
@app.route('/sign-up/', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpF(request.form)
    if request.method == 'POST':
        email = form.email.data
        username = form.username.data
        password = form.password.data
        usuario = Usuario(email, username, generate_password_hash(password, "sha256")) 

        #Esto sirve para que no se creen usuarios con email o username repetidos, regresa la página de registro si se ingresa un input repetido
        email_const = Usuario.query.filter_by(email=email).first()
        user_const = Usuario.query.filter_by(username=username).first()

        if (email_const is not None):
            if (email == email_const.email):
                return render_template('signup.html', form=form) 
        if (user_const is not None):
            if  (username == user_const.username):
                return render_template('signup.html', form=form)  
        #Luego de verificar, se añade el usuario a la base de datos con add(usuario) y commit()
        db.session.add(usuario)
        db.session.commit()
        #El usuario ahora está en sesión y será recordado como activo al irse a otras rutas
        login_user(usuario, remember=True)
        #Luego de registrarse te lleva directamente a la página de inicio
        return redirect(url_for("login.inicio"))
    #si el método es 'GET' renderiza el template signup.html
    elif request.method == 'GET':
        return render_template("signup.html", form=form)


#READ
#Tercera ruta - login. Se muestra el template login.html
#Asignamos el formulario que se va a mostrar en la página LoginF
#Si el método es post, se realiza una consulta query y si se encuentra que el usuario ingresado en el formulario existe, se loggea el usuario
# y te redirige a la ruta de /inicio
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = forms.LoginF(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        usuario = Usuario.query.filter_by(username = username).first()

        if (usuario is not None):
            if check_password_hash(usuario.password_hashed, password):
    
                login_user(usuario, remember=True)
            return redirect(url_for("login.inicio"))
        return render_template('login.html', form=form)
    else:
        return render_template('login.html', form = form)


#Cuarta ruta - inicio. Se muestra el template index.html, página que se muestra al loggearse
#Asignamos el formulario que se va a mostrar en la página, "Bicicleta".
#Si el método es post, se agrega una nueva biciclelta con los datos ingresados en el formulario
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
            imagen = form.imagen.data,
            id_usuario = current_user.email
        )
        db.session.add(bicicleta)
        db.session.commit()

        #El subquery sirve para poner en blanco los inputs cada vez que se envía un formulario
        #o se actualiza la página
        subquery = db.session.query(Bicicleta.id).filter(Bicicleta.id_usuario == current_user.email).scalar_subquery()
        p = Bicicleta.query.filter(Bicicleta.id.in_(subquery)).all()
        if p is not None:
            return redirect('inicio')

    subquery = db.session.query(Bicicleta.id).filter(Bicicleta.id_usuario == current_user.email).scalar_subquery()
    p = Bicicleta.query.filter(Bicicleta.id.in_(subquery)).all()
    usuario = current_user
    return render_template('Index.html', form = form, bicicletas = p, usuario=usuario)

#Controllers

#UPDATE BICICLETA
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
        bicicleta.imagen = form.imagen.data
        db.session.commit()
        return redirect(url_for("login.inicio"))
    bicicleta = Bicicleta.query.filter(Bicicleta.id == id).one_or_none()
    return render_template('actualizar.html', form = form, id=id, bicicleta=bicicleta)

#DELETE BICICLETA
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

#Cierra la sesión del usuario
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('.login'))
