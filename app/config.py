# Código para armazenar variáveis do sistena

class Config:
    UPLOAD_FOLDER = 'uploads'
    PROCESSED_FOLDER = 'processed'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGHT = 16 * 1024 * 1024
    SECRET_KEY = 'secret_key'