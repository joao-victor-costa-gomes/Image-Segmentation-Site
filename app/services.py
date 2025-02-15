import os
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename

from app.segmentation.thresholding import apply_multiple_thresholds, apply_threshold

def ensure_folder_exists(folder_path):
    """ Garante que a pasta existe, se não, cria. """
    os.makedirs(folder_path, exist_ok=True)

def save_uploaded_image(file):
    """ Salva a imagem enviada pelo usuário na pasta uploads/ e retorna o caminho do arquivo. """
    if file and file.filename != '':
        file_extension = os.path.splitext(secure_filename(file.filename))[1]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"image_{timestamp}{file_extension}"

        upload_folder = current_app.config['UPLOAD_FOLDER']
        ensure_folder_exists(upload_folder)  # Certifica-se de que a pasta existe
        upload_path = os.path.join(upload_folder, filename)

        file.save(upload_path)
        return filename  # Retorna o nome do arquivo salvo

    return None

def apply_segmentation(filename, method, threshold_value):
    """ Aplica um método de segmentação na imagem e retorna os arquivos processados. """
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    # Seleciona o método de segmentação
    if method == "threshold":
        #return apply_multiple_thresholds(upload_path, threshold_value)

        # Chama a função que gera múltiplas imagens segmentadas
        segmented_files = apply_multiple_thresholds(upload_path, threshold_value)

        # Nomes correspondentes para os métodos aplicados
        method_names = [
            "Threshold Binário",
            "Threshold Binário Invertido",
            "Threshold Truncado",
            "Threshold para Zero",
            "Threshold para Zero Invertido"
        ]

        # Retorna uma lista de dicionários com os nomes e métodos
        return [{"filename": segmented_files[i], "method": method_names[i]} for i in range(len(segmented_files))]


    # Outros métodos podem ser adicionados aqui futuramente

    return []