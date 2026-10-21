from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    def __init__(self, data):
        # Mapeo de los atributos de la entidad usuario desde la base de datos
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.edad = data['edad']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def guardar(cls, data):
        # Registra un nuevo usuario cifrando previamente su contraseña
        query = "INSERT INTO usuarios (nombre, apellido, email, edad, password, created_at, updated_at) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(edad)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('querido_diario_db').query_db(query, data)

    @classmethod
    def obtener_por_email(cls, email):
        # Busca un usuario por su correo electrónico para procesos de autenticación
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL('querido_diario_db').query_db(query, {'email': email})
        if not resultado:
            return False
        return cls(resultado[0])

    @classmethod
    def obtener_por_id(cls, user_id):
        # Recupera los datos de un usuario específico según su identificador único
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultado = connectToMySQL('querido_diario_db').query_db(query, {'id': user_id})
        if not resultado:
            return False
        return cls(resultado[0])

    @staticmethod
    def validar_registro(formulario):
        # Valida los campos del formulario de registro antes de permitir el acceso
        is_valid = True
        
        # Validar longitud mínima de nombre y apellido
        if len(formulario['nombre']) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            is_valid = False
        if len(formulario['apellido']) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            is_valid = False

        # Validar formato y disponibilidad del correo electrónico
        if not EMAIL_REGEX.match(formulario['email']):
            flash("Formato de correo electrónico inválido.", "registro")
            is_valid = False
        else:
            usuario_existente = Usuario.obtener_por_email(formulario['email'])
            if usuario_existente:
                flash("El correo electrónico ya está registrado.", "registro")
                is_valid = False

        # Validar restricción de edad mínima (al menos 18 años)
        if formulario['edad'] == "":
            flash("La edad es obligatoria.", "registro")
            is_valid = False
        elif int(formulario['edad']) < 18:
            flash("Debes tener al menos 18 años para registrarte.", "registro")
            is_valid = False

        # Validar longitud y coincidencia de contraseñas
        if len(formulario['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "registro")
            is_valid = False
        elif formulario['password'] != formulario['confirm_password']:
            flash("Las contraseñas no coinciden.", "registro")
            is_valid = False

        return is_valid