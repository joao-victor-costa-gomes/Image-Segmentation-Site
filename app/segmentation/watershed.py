import os
import cv2
import numpy as np
from flask import current_app

def watershed(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return None

    # Converter para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar filtro para remover ruídos e melhorar bordas
    blurred = cv2.medianBlur(gray, 5)

    # Aplicar um threshold binário para destacar objetos
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Encontrar os marcadores para Watershed
    kernel = np.ones((3, 3), np.uint8)
    sure_bg = cv2.dilate(thresh, kernel, iterations=3)  # Definir fundo certo

    # Aplicar distância transform para encontrar o centro dos objetos
    dist_transform = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    # Encontrar regiões desconhecidas (possíveis bordas)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Marcar objetos com labels diferentes
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1  # Para que o fundo seja marcado como 1
    markers[unknown == 255] = 0  # Definir bordas como 0

    # Aplicar Watershed
    markers = cv2.watershed(image, markers)
    image[markers == -1] = [0, 0, 255]  # Marcar as bordas em vermelho

    # Criar a pasta para salvar os arquivos processados
    processed_folder = current_app.config['PROCESSED_FOLDER']
    os.makedirs(processed_folder, exist_ok=True)

    # Nome do arquivo segmentado
    segmented_filename = f"watershed_{os.path.basename(image_path)}"
    processed_path = os.path.join(processed_folder, segmented_filename)

    # Salvar a imagem segmentada
    cv2.imwrite(processed_path, image)

    segmented_filenames = {}
    segmented_filenames["Com Watershed"] = segmented_filename

    return segmented_filenames  # Retorna o nome do arquivo segmentado
