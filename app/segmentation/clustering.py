import cv2
import numpy as np
import os
from flask import current_app

def kmeans(image_path, k=3, attempts=10):
    """
    Aplica segmentação de imagem usando K-Means Clustering.

    Parâmetros:
        - image_path (str): Caminho da imagem original.
        - k (int): Número de clusters para segmentação.
        - attempts (int): Número de tentativas para encontrar melhores centroides.

    Retorna:
        - Nome do arquivo segmentado.
    """
    image = cv2.imread(image_path)

    if image is None:
        return None

    # Converter a imagem para espaço de cor RGB (caso esteja em BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Obtém as dimensões da imagem
    h, w, c = image.shape

    # Transforma a imagem em um vetor de pixels (Nx3)
    pixels = image.reshape((-1, 3))  # Reshape para vetor de pixels (altura * largura, 3)
    pixels = np.float32(pixels)  # Converte para float32 (necessário para K-Means)

    # Critério de parada do K-Means: 10 iterações ou precisão de 1.0
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Aplica o K-Means
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, attempts, cv2.KMEANS_RANDOM_CENTERS)

    # Converte os centroides (cores médias dos clusters) para uint8
    centers = np.uint8(centers)

    # Mapeia os pixels para a cor do seu cluster correspondente
    segmented_image = centers[labels.flatten()]

    # Reformata a imagem segmentada para as dimensões originais
    segmented_image = segmented_image.reshape((h, w, c))

    # Criar a pasta para salvar os arquivos processados
    processed_folder = current_app.config['PROCESSED_FOLDER']
    os.makedirs(processed_folder, exist_ok=True)

    # Nome do arquivo segmentado
    segmented_filename = f"kmeans_{k}_clusters_{os.path.basename(image_path)}"
    processed_path = os.path.join(processed_folder, segmented_filename)

    # Salvar a imagem segmentada
    cv2.imwrite(processed_path, cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR))

    segmented_filenames = {}
    segmented_filenames["Segmentação K-Means"] = segmented_filename

    return segmented_filenames  # Retorna o nome do arquivo segmentado
