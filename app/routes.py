import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory  

# Criando um Blueprint para as rotas da aplicação 
main = Blueprint('main', __name__)

@main.route('/')
def home_page():
    return render_template('home.html')

@main.route('/threshold', methods=['GET', 'POST'])
def threshold_page():

    filename = None

    if 'image' not in request.files:
        return render_template('threshold.html', filename=None)

    file = request.files['image']

    if file.filename == '':
        return render_template('threshold.html', filename=None)

    # Segurança do arquivo enviada
    file_extension = os.path.splitext(secure_filename(file.filename))[1]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"image_{timestamp}{file_extension}"

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)  # Garante que a pasta exista
    upload_path = os.path.join(upload_folder, filename)

    # Salva a imagem na pasta uploads
    file.save(upload_path)

    return render_template('threshold.html', filename=filename)

# Rota para servir os arquivos da pasta uploads/
@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)