import os
import cv2
from flask import current_app

def threshold(image_path, threshold_value=128, block_size=11, c_value=2):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        return []

    # Criar a pasta para salvar os arquivos processados
    processed_folder = current_app.config['PROCESSED_FOLDER']
    os.makedirs(processed_folder, exist_ok=True)

    segmented_filenames = {}

    # Thresholding Binário
    _, binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    binary_filename = f"binary_{os.path.basename(image_path)}"
    cv2.imwrite(os.path.join(processed_folder, binary_filename), binary_image)
    segmented_filenames["Threshold Binário"] = binary_filename

    # Otsu's Thresholding
    _, otsu_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    otsu_filename = f"otsu_{os.path.basename(image_path)}"
    cv2.imwrite(os.path.join(processed_folder, otsu_filename), otsu_image)
    segmented_filenames["Threshold Otsu"] = otsu_filename

    # Adaptive Thresholding
    adaptive_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY, block_size, c_value)
    adaptive_filename = f"adaptive_{os.path.basename(image_path)}"
    cv2.imwrite(os.path.join(processed_folder, adaptive_filename), adaptive_image)
    segmented_filenames["Threshold Adaptativo"] = adaptive_filename

    return segmented_filenames  # Retorna um dicionário com os nomes dos arquivos segmentados