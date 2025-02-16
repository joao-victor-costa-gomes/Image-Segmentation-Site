import os
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename

from app.segmentation.thresholding import threshold

def ensure_folder_exists(folder_path):
    """ Garante que a pasta existe, se não, cria. """
    os.makedirs(folder_path, exist_ok=True)

def save_uploaded_image(file):
    """ Salva a imagem enviada pelo usuário na pasta uploads/ e retorna o caminho do arquivo. """
    if file and file.filename != '':
        file_extension = os.path.splitext(secure_filename(file.filename))[1]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}{file_extension}"

        upload_folder = current_app.config['UPLOAD_FOLDER']
        ensure_folder_exists(upload_folder)  
        upload_path = os.path.join(upload_folder, filename)

        file.save(upload_path)
        return filename  # Retorna o nome do arquivo salvo

    return None


# ----------------- MÉTODOS DE SEGMENTAÇÃO -----------------


def apply_threshold(filename, threshold_value, block_size, c_value):
    """Aplica múltiplas variações de thresholding na imagem."""
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    # Aplica múltiplos métodos de threshold e obtém um dicionário de arquivos segmentados
    segmented_files = threshold(upload_path, threshold_value, block_size, c_value)

    # Retorna lista de dicionários com os arquivos e nomes dos métodos aplicados
    return [{"filename": segmented_files[key], "method": key} for key in segmented_files]
