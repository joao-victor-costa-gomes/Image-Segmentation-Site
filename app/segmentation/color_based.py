import os
import cv2
import numpy as np
from flask import current_app

def color_based(image_path, lower_bound, upper_bound):
    """
    Aplica segmentação baseada em cores utilizando HSV e gera duas imagens:
        - A segmentação normal.
        - A imagem em preto e branco mantendo apenas a parte segmentada colorida.

    Parâmetros:
        - image_path (str): Caminho da imagem original.
        - lower_bound (tuple): Limite inferior da cor no formato (H, S, V).
        - upper_bound (tuple): Limite superior da cor no formato (H, S, V).

    Retorna:
        - Dicionário com os nomes das imagens segmentadas.
    """
    image = cv2.imread(image_path)

    if image is None:
        return None

    # Converter de BGR para HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Criar a máscara dentro do intervalo de cor definido
    mask = cv2.inRange(hsv_image, np.array(lower_bound), np.array(upper_bound))

    # Criar a imagem segmentada
    segmented_image = cv2.bitwise_and(image, image, mask=mask)

    # Criar uma versão em preto e branco da imagem original
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayscale_colored = cv2.cvtColor(grayscale, cv2.COLOR_GRAY2BGR)  # Converter para 3 canais

    # Aplicar a máscara na imagem preto e branco (mantendo apenas a área segmentada colorida)
    bw_segmented = np.where(mask[:, :, None] == 255, image, grayscale_colored)

    # Criar a pasta para salvar os arquivos processados
    processed_folder = current_app.config['PROCESSED_FOLDER']
    os.makedirs(processed_folder, exist_ok=True)

    # Salvar a imagem segmentada normal
    segmented_filename = f"color_segmented_{os.path.basename(image_path)}"
    cv2.imwrite(os.path.join(processed_folder, segmented_filename), segmented_image)

    # Salvar a imagem preto e branco com apenas a parte segmentada colorida
    bw_segmented_filename = f"bw_segmented_{os.path.basename(image_path)}"
    cv2.imwrite(os.path.join(processed_folder, bw_segmented_filename), bw_segmented)

    segmented_filenames = {
        "HSV/LAB": segmented_filename,
        "BW Color Retained": bw_segmented_filename
    }

    return segmented_filenames  # Retorna os nomes dos arquivos segmentados
