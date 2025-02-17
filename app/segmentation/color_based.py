import os
import cv2
import numpy as np
from flask import current_app

def color_based(image_path, lower_bound, upper_bound):
    """
    Aplica segmentação baseada em cores utilizando HSV.

    Parâmetros:
        - image_path (str): Caminho da imagem original.
        - lower_bound (tuple): Limite inferior da cor no formato (H, S, V).
        - upper_bound (tuple): Limite superior da cor no formato (H, S, V).

    Retorna:
        - Nome do arquivo segmentado.
    """
    image = cv2.imread(image_path)

    if image is None:
        return None

    # Converter de BGR para HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Criar a máscara dentro do intervalo de cor definido
    mask = cv2.inRange(hsv_image, np.array(lower_bound), np.array(upper_bound))

    # Aplicar a máscara sobre a imagem original
    segmented_image = cv2.bitwise_and(image, image, mask=mask)

    # Criar a pasta para salvar os arquivos processados
    processed_folder = current_app.config['PROCESSED_FOLDER']
    os.makedirs(processed_folder, exist_ok=True)

    # Nome do arquivo segmentado
    segmented_filename = f"color_segmented_{os.path.basename(image_path)}"
    processed_path = os.path.join(processed_folder, segmented_filename)

    # Salvar a imagem segmentada
    cv2.imwrite(processed_path, segmented_image)

    segmented_filenames = {}
    segmented_filenames["HSV/LAB"] = segmented_filename

    return segmented_filenames  # Retorna o nome do arquivo segmentado