import os
from flask import Flask

# Carregando nossas variáveis da aplicação
from app.config import Config

def create_app():
    # Criando uma aplicação Flask
    app = Flask(__name__)

    # Carregando nossas variáveis da aplicação
    app.config.from_object(Config)

    # Criar a pasta uploads/ se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Registrando a Blueprint de rotas nessa aplicação
    from app.routes import main
    app.register_blueprint(main)

    # Retornando a aplicação
    return app