from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime

class Entrada:
    def __init__(self, data):
        self.id = data['id']
        self.fecha = data['fecha']
        self.notas = data['notas']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.nombre_usuario = data.get('nombre', '')

    @classmethod
    def guardar(cls, data):
        query = "INSERT INTO entradas (fecha, notas, user_id, created_at, updated_at) VALUES (%(fecha)s, %(notas)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL('querido_diario_db').query_db(query, data)

    @classmethod
    def obtener_por_usuario(cls, user_id):
        query = "SELECT * FROM entradas WHERE user_id = %(user_id)s ORDER BY fecha DESC, id DESC;"
        resultados = connectToMySQL('querido_diario_db').query_db(query, {'user_id': user_id})
        entradas = []
        if resultados:
            for fila in resultados:
                entradas.append(cls(fila))
        return entradas

    @classmethod
    def obtener_por_id(cls, entrada_id):
        query = "SELECT * FROM entradas WHERE id = %(id)s;"
        resultado = connectToMySQL('querido_diario_db').query_db(query, {'id': entrada_id})
        if not resultado:
            return False
        return cls(resultado[0])

    @classmethod
    def actualizar(cls, data):
        query = "UPDATE entradas SET fecha = %(fecha)s, notas = %(notas)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('querido_diario_db').query_db(query, data)

    @classmethod
    def borrar(cls, entrada_id):
        query = "DELETE FROM entradas WHERE id = %(id)s;"
        return connectToMySQL('querido_diario_db').query_db(query, {'id': entrada_id})

    @classmethod
    def buscar_por_notas(cls, termino, user_id):
        # Usamos CHAR(37) para que MySQL genere el '%' y Python nunca lo toque, evitando errores de conector
        query = "SELECT * FROM entradas WHERE user_id = %(user_id)s AND notas LIKE CONCAT(CHAR(37), %(termino)s, CHAR(37)) ORDER BY fecha DESC;"
        data = {
            'user_id': user_id,
            'termino': termino
        }
        resultados = connectToMySQL('querido_diario_db').query_db(query, data)
        
        entradas = []
        if resultados:
            for fila in resultados:
                entradas.append(cls(fila))
        return entradas

    @staticmethod
    def validar_entrada(formulario):
        is_valid = True

        if not formulario['notas'].strip():
            flash("Las notas no pueden estar vacías.", "entrada")
            is_valid = False

        if not formulario['fecha']:
            flash("La fecha es obligatoria.", "entrada")
            is_valid = False
        else:
            fecha_ingresada = datetime.strptime(formulario['fecha'], '%Y-%m-%d').date()
            fecha_actual = datetime.now().date()
            if fecha_ingresada > fecha_actual:
                flash("No puedes crear una entrada con fecha en el futuro.", "entrada")
                is_valid = False

        return is_valid