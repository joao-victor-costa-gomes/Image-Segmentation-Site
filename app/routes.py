import os
from flask import Blueprint, render_template, request, current_app, send_from_directory, redirect, url_for
from app.services import save_uploaded_image, ensure_folder_exists

from app.services import apply_threshold
# Criando um Blueprint contendo todas essas rotas abaixo
main = Blueprint('main', __name__)

@main.route('/')
def home_page():
    return render_template('home.html')

# Rota para servir os arquivos da pasta uploads/
@main.route('/uploads/<filename>')
def uploaded_file_path(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

# Rota para servir os arquivos da pasta processed/
@main.route('/processed/<filename>')
def processed_file_path(filename):
    return send_from_directory(current_app.config['PROCESSED_FOLDER'], filename)

@main.route('/threshold', methods=['GET', 'POST'])
def threshold_page():
    filename = None
    segmented_filenames = None

    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            filename = save_uploaded_image(file)  

        if 'apply_threshold' in request.form:
            # PEGANDO PARÂMETROS
            filename = request.form.get('filename')
            threshold_value = request.form.get('threshold_value', type=int)
            block_size = request.form.get('block_size', type=int)
            c_value = request.form.get('c_value', type=int)

            if filename and threshold_value is not None:
                # APLICANDO MÉTODO DE SEGMENTAÇÃO
                segmented_filenames = apply_threshold(filename, threshold_value, block_size, c_value)

                if segmented_filenames:
                    ensure_folder_exists(current_app.config['PROCESSED_FOLDER'])  

    return render_template('threshold.html', filename=filename, segmented_filenames=segmented_filenames)