# Configuracion inicial de la app Flask y carga de claves desde el .env
import os
from flask import Flask
from dotenv import load_dotenv

# Cargamos las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Importamos los controladores aquí abajo para que reconozcan la app
from flask_app.controllers import controlador_usuarios, controlador_entradas