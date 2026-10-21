from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    # Si el usuario ya inició sesión, lo redirige al dashboard principal
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    # Valida los campos del formulario de registro antes de procesar
    if not Usuario.validar_registro(request.form):
        return redirect('/')
    
    # Encripta la contraseña de forma segura usando Bcrypt
    password_hash = bcrypt.generate_password_hash(request.form['password'])
    
    # Prepara el diccionario de datos para la inserción en la base de datos
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "edad": request.form['edad'],
        "password": password_hash
    }
    
    # Guarda el usuario y almacena sus credenciales en la sesión activa
    user_id = Usuario.guardar(data)
    session['user_id'] = user_id
    session['nombre_usuario'] = request.form['nombre']
    
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    # Busca al usuario en la base de datos mediante su correo electrónico
    usuario_en_db = Usuario.obtener_por_email(request.form['email'])
    
    # Valida si el correo existe
    if not usuario_en_db:
        flash("Correo electrónico no registrado.", "login")
        return redirect('/')
    
    # Valida que la contraseña coincida con el hash almacenado
    if not bcrypt.check_password_hash(usuario_en_db.password, request.form['password']):
        flash("Contraseña incorrecta.", "login")
        return redirect('/')
    
    # Establece las variables de sesión tras un inicio de sesión exitoso
    session['user_id'] = usuario_en_db.id
    session['nombre_usuario'] = usuario_en_db.nombre
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    # Cierra la sesión limpiando todas las variables almacenadas
    session.clear()
    return redirect('/')