import os
import cv2
from flask import current_app

def canny_edge(image_path, min_val=50, max_val=150):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        return None

    # Criar a pasta para salvar os arquivos processados
    processed_folder = current_app.config['PROCESSED_FOLDER']
    os.makedirs(processed_folder, exist_ok=True)

    segmented_filenames = {}

    # Aplicar o detector de bordas de Canny
    edges = cv2.Canny(image, min_val, max_val)

    # Nome do arquivo segmentado
    segmented_filename = f"canny_{os.path.basename(image_path)}"
    processed_path = os.path.join(processed_folder, segmented_filename)

    # Salvar a imagem segmentada
    cv2.imwrite(processed_path, edges)
    segmented_filenames["Detector de Canny"] = segmented_filename

    return segmented_filenames  # Retorna o nome do arquivo processado
