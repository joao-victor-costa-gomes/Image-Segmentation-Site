import os
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename

# Importando algoritmos
from app.segmentation.thresholding import threshold
from app.segmentation.edge_based import canny_edge
from app.segmentation.region_based import region_based

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

# Thresholding
def apply_threshold(filename, threshold_value, block_size, c_value):
    """Aplica múltiplas variações de thresholding na imagem."""
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    # Aplica múltiplos métodos de threshold e obtém um dicionário de arquivos segmentados
    segmented_files = threshold(upload_path, threshold_value, block_size, c_value)

    # Retorna lista de dicionários com os arquivos e nomes dos métodos aplicados
    return [{"filename": segmented_files[key], "method": key} for key in segmented_files]

# Edge-based 
def apply_canny_edge(filename, min_val, max_val):
    """Aplica múltiplas variações de thresholding na imagem."""
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    # Aplica múltiplos métodos de threshold e obtém um dicionário de arquivos segmentados
    segmented_files = canny_edge(upload_path, min_val, max_val)

    # Retorna lista de dicionários com os arquivos e nomes dos métodos aplicados
    return [{"filename": segmented_files[key], "method": key} for key in segmented_files]

# Region-based 
def apply_region_based(filename,num_regions):
    """Aplica múltiplas variações de thresholding na imagem."""
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    # Aplica múltiplos métodos de threshold e obtém um dicionário de arquivos segmentados
    segmented_files = region_based(upload_path, num_regions)

    # Retorna lista de dicionários com os arquivos e nomes dos métodos aplicados
    return [{"filename": segmented_files[key], "method": key} for key in segmented_files]