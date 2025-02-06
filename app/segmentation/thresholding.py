import os
import cv2
import numpy as np
from flask import current_app

def apply_threshold(image_path, threshold_value):
    # Lê a imagem em escala de cinza
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        return []

    # Aplica o thresholding binário
    _, thresholded_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)

    # Define o caminho para salvar a imagem segmentada
    processed_folder = current_app.config['PROCESSED_FOLDER']
    os.makedirs(processed_folder, exist_ok=True)  # Garante que a pasta exista
    
    segmented_filename = f"segmented_{os.path.basename(image_path)}"
    processed_path = os.path.join(processed_folder, segmented_filename)

    # Salva a imagem segmentada na pasta processed/
    cv2.imwrite(processed_path, thresholded_image)

    return [segmented_filename]  # Retorna uma lista, mesmo que tenha um único elemento


def apply_multiple_thresholds(image_path, threshold_value):
    # Lê a imagem em escala de cinza
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        return []

    # Definição dos métodos de threshold disponíveis
    threshold_methods = {
        "binary": cv2.THRESH_BINARY,
        "binary_inv": cv2.THRESH_BINARY_INV,
        "trunc": cv2.THRESH_TRUNC,
        "tozero": cv2.THRESH_TOZERO,
        "tozero_inv": cv2.THRESH_TOZERO_INV
    }

    # Criar a pasta para salvar os arquivos processados
    processed_folder = current_app.config['PROCESSED_FOLDER']
    os.makedirs(processed_folder, exist_ok=True)

    segmented_filenames = []

    # Aplicar cada método de threshold e salvar o resultado
    for method_name, method in threshold_methods.items():
        _, thresholded_image = cv2.threshold(image, threshold_value, 255, method)

        # Nome do arquivo segmentado
        segmented_filename = f"{method_name}_{os.path.basename(image_path)}"
        processed_path = os.path.join(processed_folder, segmented_filename)

        # Salvar a imagem segmentada
        cv2.imwrite(processed_path, thresholded_image)

        # Adicionar à lista de arquivos segmentados
        segmented_filenames.append(segmented_filename)

    return segmented_filenames  # Retorna a lista com todas as imagens segmentadas