import os
import cv2

def apply_binary_threshold(image_path, threshold_value, output_folder):
    # Carregar a imagem em escala de cinza
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("ERROR: Imagem não encontrada ou não pôde ser carregada.")

    # Aplicar a segmentação por limiarização
    _, thresholded_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)

    # Nome do arquivo de saída
    output_filename = os.path.basename(image_path)
    output_path = os.path.join(output_folder, output_filename)

    # Garantir que a pasta de saída existe
    os.makedirs(output_folder, exist_ok=True)

    # Salvar a imagem processada
    cv2.imwrite(output_path, thresholded_image)

    return output_path
