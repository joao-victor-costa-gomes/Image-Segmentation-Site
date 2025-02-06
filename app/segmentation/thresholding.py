import cv2
import os
import numpy as np
from flask import current_app

def apply_threshold(image_path, threshold_value):
    """
    Aplica um thresholding binário em uma imagem e salva o resultado.
    
    :param image_path: Caminho da imagem original.
    :param threshold_value: Valor do threshold (0-255).
    :return: Nome do arquivo segmentado salvo.
    """
    # Lê a imagem em escala de cinza
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        return None

    # Aplica o thresholding binário
    _, thresholded_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)

    # Define o caminho para salvar a imagem segmentada
    processed_folder = current_app.config['PROCESSED_FOLDER']
    os.makedirs(processed_folder, exist_ok=True)  # Garante que a pasta exista
    
    segmented_filename = f"segmented_{os.path.basename(image_path)}"
    processed_path = os.path.join(processed_folder, segmented_filename)

    # Salva a imagem segmentada na pasta processed/
    cv2.imwrite(processed_path, thresholded_image)

    return segmented_filename
