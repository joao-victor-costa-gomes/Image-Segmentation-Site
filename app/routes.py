import os
import cv2
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory  

from .segmentation.thresholding import apply_threshold

# Criando um Blueprint para as rotas da aplicação 
main = Blueprint('main', __name__)

@main.route('/')
def home_page():
    return render_template('home.html')

@main.route('/threshold', methods=['GET', 'POST'])
def threshold_page():
    filename = None
    segmented_filename = None

    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']

            if file and file.filename != '':  # Verifica se o arquivo realmente foi enviado
                # Segurança do nome do arquivo
                file_extension = os.path.splitext(secure_filename(file.filename))[1]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"image_{timestamp}{file_extension}"

                upload_folder = current_app.config['UPLOAD_FOLDER']
                os.makedirs(upload_folder, exist_ok=True)  # Garante que a pasta exista
                upload_path = os.path.join(upload_folder, filename)

                # Salva a imagem na pasta uploads
                file.save(upload_path)

        if 'apply_threshold' in request.form:
            filename = request.form.get('filename')
            threshold_value = request.form.get('threshold_value', type=int)

            if filename and threshold_value is not None:
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

                # Aplica o thresholding na imagem
                segmented_filename = apply_threshold(upload_path, threshold_value)

                if segmented_filename:
                    processed_folder = current_app.config['PROCESSED_FOLDER']
                    os.makedirs(processed_folder, exist_ok=True)  # Garante que a pasta exista
                    processed_path = os.path.join(processed_folder, segmented_filename)


    # Retorna a página juntamente com a imagem enviada e a processada
    return render_template('threshold.html', filename=filename, segmented_filename=segmented_filename)

# Rota para servir os arquivos da pasta uploads/
@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

# Rota para servir os arquivos da pasta processed/
@main.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(current_app.config['PROCESSED_FOLDER'], filename)
