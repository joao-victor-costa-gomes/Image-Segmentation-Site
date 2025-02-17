import os
import cv2
import numpy as np
from flask import current_app

def flattern_img(img):
    """ Transforma a imagem 2D em um vetor de pixels. """
    altura, largura = img.shape[:2]
    return img.reshape(altura * largura, 3)  # Mantém os 3 canais de cor

def segmenta_regioes(img, num_regions=3):
    """
    Segmenta a imagem em um número definido de regiões, utilizando tons de cinza.

    Parâmetros:
        - img (np.array): Imagem original carregada com OpenCV.
        - num_regions (int): Número de regiões para segmentação.

    Retorna:
        - Imagem segmentada com tons de cinza.
    """
    pixels = flattern_img(img).copy()
    seg_regiao = np.zeros_like(pixels)  # Inicializa a imagem de saída

    thresholds = np.linspace(0, 1, num_regions + 1)  # Define os intervalos para segmentação

    # Criar tons de cinza com base no número de regiões
    grayscale_values = np.linspace(0, 255, num_regions, dtype=np.uint8)

    for i in range(len(pixels)):
        mean_pixel = pixels[i].mean() / 255.0  # Normaliza para faixa [0, 1]

        # Encontra em qual faixa o pixel se encaixa
        for j in range(num_regions):
            if thresholds[j] <= mean_pixel < thresholds[j + 1]:
                seg_regiao[i] = [grayscale_values[j]] * 3  # Aplica o tom de cinza
                break

    seg_regiao = seg_regiao.reshape(img.shape[0], img.shape[1], 3)
    return seg_regiao

def save_segmented_image(image_path, segmented_image, method_name):
    """
    Salva a imagem segmentada na pasta processed/.

    Parâmetros:
        - image_path (str): Caminho da imagem original.
        - segmented_image (np.array): Imagem segmentada.
        - method_name (str): Nome do método para o nome do arquivo.

    Retorna:
        - Nome do arquivo salvo.
    """
    processed_folder = current_app.config['PROCESSED_FOLDER']
    os.makedirs(processed_folder, exist_ok=True)

    segmented_filename = f"{method_name}_{os.path.basename(image_path)}"
    processed_path = os.path.join(processed_folder, segmented_filename)

    cv2.imwrite(processed_path, segmented_image)

    segmented_filenames = {}
    segmented_filenames["Regiões"] = segmented_filename

    return segmented_filenames  # Retorna o nome do arquivo salvo

def region_based(image_path, num_regions=3):
    """
    Aplica segmentação baseada em regiões e salva a imagem.

    Parâmetros:
        - image_path (str): Caminho da imagem original.
        - num_regions (int): Número de regiões para segmentação.

    Retorna:
        - Nome do arquivo segmentado.
    """
    img = cv2.imread(image_path)
    if img is None:
        return None

    # Converter para escala de cinza
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)  # Mantém 3 canais

    # Aplicar segmentação
    segmented_img = segmenta_regioes(img_gray, num_regions)

    # Salvar imagem processada
    return save_segmented_image(image_path, segmented_img, f"region_{num_regions}_regions_gray")
