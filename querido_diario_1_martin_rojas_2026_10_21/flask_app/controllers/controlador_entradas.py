from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.entrada import Entrada

@app.route('/dashboard')
def dashboard():
    # Valida que exista una sesión activa antes de mostrar el panel principal
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder al dashboard.", "login")
        return redirect('/')
    
    # Carga únicamente las entradas del usuario logueado
    entradas = Entrada.obtener_por_usuario(session['user_id'])
    
    return render_template('dashboard.html', entradas=entradas)

@app.route('/nueva')
def nueva_entrada_form():
    # Protege la ruta para requerir inicio de sesión
    if 'user_id' not in session:
        flash("Debes iniciar sesión para crear una entrada.", "login")
        return redirect('/')
    return render_template('nueva_entrada.html')

@app.route('/crear/entrada', methods=['POST'])
def crear_entrada():
    # Comprobación de seguridad de sesión
    if 'user_id' not in session:
        return redirect('/')
    
    # Valida los campos y la restricción de fechas futuras
    if not Entrada.validar_entrada(request.form):
        return redirect('/nueva')
    
    # Prepara los datos asociándolos al usuario actual
    data = {
        "fecha": request.form['fecha'],
        "notas": request.form['notas'],
        "user_id": session['user_id']
    }
    
    Entrada.guardar(data)
    return redirect('/dashboard')

@app.route('/ver/<int:id>')
def ver_entrada(id):
    if 'user_id' not in session:
        return redirect('/')
    
    entrada = Entrada.obtener_por_id(id)
    if not entrada:
        flash("La entrada no existe.", "dashboard")
        return redirect('/dashboard')
    
    # Seguridad (Bonus): Evita que el usuario vea entradas ajenas alterando la URL
    if entrada.user_id != session['user_id']:
        flash("No tienes permiso para ver esta entrada.", "dashboard")
        return redirect('/dashboard')
        
    return render_template('ver_entrada.html', entrada=entrada)

@app.route('/editar/<int:id>')
def editar_entrada_form(id):
    if 'user_id' not in session:
        return redirect('/')
        
    entrada = Entrada.obtener_por_id(id)
    if not entrada:
        return redirect('/dashboard')
        
    # Seguridad (Bonus): Valida propiedad antes de permitir la edición
    if entrada.user_id != session['user_id']:
        flash("No tienes permiso para editar esta entrada.", "dashboard")
        return redirect('/dashboard')
        
    return render_template('editar_entrada.html', entrada=entrada)

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_entrada(id):
    if 'user_id' not in session:
        return redirect('/')
        
    entrada = Entrada.obtener_por_id(id)
    # Verifica existencia y propiedad del recurso
    if not entrada or entrada.user_id != session['user_id']:
        return redirect('/dashboard')
        
    # Aplica las mismas validaciones de negocio que en la creación
    if not Entrada.validar_entrada(request.form):
        return redirect(f'/editar/{id}')
        
    data = {
        "id": id,
        "fecha": request.form['fecha'],
        "notas": request.form['notas']
    }
    Entrada.actualizar(data)
    return redirect('/dashboard')

@app.route('/borrar/<int:id>')
def borrar_entrada(id):
    if 'user_id' not in session:
        return redirect('/')
        
    entrada = Entrada.obtener_por_id(id)
    # Seguridad (Bonus): Valida estrictamente que la entrada pertenezca al usuario antes de borrar
    if entrada and entrada.user_id == session['user_id']:
        Entrada.borrar(id)
        
    return redirect('/dashboard')

@app.route('/buscar/<string:termino>')
def buscar_entradas(termino):
    if 'user_id' not in session:
        return redirect('/')
        
    entradas = Entrada.buscar_por_notas(termino, session['user_id'])
    return render_template('buscar.html', entradas=entradas, termino=termino)