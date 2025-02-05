# Código para armazenar variáveis do sistena

import os

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Diretório do projeto
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')  # Caminho absoluto para uploads/
    PROCESSED_FOLDER = os.path.join(BASE_DIR, 'processed')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    SECRET_KEY = 'secret_key'
