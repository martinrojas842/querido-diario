# Archivo principal para arrancar el servidor de Flask
from flask_app import app
from flask_app.controllers import controlador_usuarios, controlador_entradas

if __name__ == "__main__":
    app.run(debug=True)