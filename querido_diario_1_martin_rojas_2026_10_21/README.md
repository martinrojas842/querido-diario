# Querido Diario

Aplicación web desarrollada en Python con Flask y MySQL bajo el patrón de arquitectura Modelo-Vista-Controlador (MVC). El sistema permite a los usuarios gestionar entradas de diario personales de forma privada, incorporando autenticación segura, validaciones del lado del servidor y filtrado dinámico.

## Autor

- **Desarrollador:** Martin Rojas

## Tecnologías Utilizadas

- **Backend:** Python, Flask
- **Base de Datos:** MySQL (phpMyAdmin)
- **Seguridad:** Flask-Bcrypt, python-dotenv
- **Frontend:** HTML5, CSS3, Bootstrap 5

## Estructura del Proyecto (MVC)

```text
Querido_Diario/
│
├── flask_app/
│   ├── config/
│   │   └── mysqlconnection.py
│   ├── controllers/
│   │   ├── controlador_entradas.py
│   │   └── controlador_usuarios.py
│   ├── models/
│   │   ├── entrada.py
│   │   └── usuario.py
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   ├── templates/
│   │   ├── buscar.html
│   │   ├── dashboard.html
│   │   ├── editar_entrada.html
│   │   ├── index.html
│   │   ├── nueva_entrada.html
│   │   └── ver_entrada.html
│   └── __init__.py
│
├── resources/
│   └── DB/
│       ├── ERD.png
│       └── querido_diario.sql
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── run.py