import os
import cv2
import numpy as np
from collections import deque
from flask import current_app


def region_growing(image, seed_point, threshold=10):
    """
    Segmentação por Region Growing.

    Parâmetros:
    - image: Imagem de entrada em escala de cinza ou RGB
    - seed_point: Tupla (x, y) indicando o ponto semente
    - threshold: Limiar de diferença de intensidade para crescimento

    Retorna:
    - mask: Máscara com a região segmentada
    """

    # Converte para escala de cinza se for RGB
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    h, w = gray.shape
    mask = np.zeros((h, w), dtype=np.uint8)

    # Fila para processar pixels
    queue = deque()
    queue.append(seed_point)

    # Intensidade do ponto semente
    seed_intensity = gray[seed_point[1], seed_point[0]]

    # Vetores para checar vizinhos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4-connectividade

    while queue:
        x, y = queue.popleft()

        if mask[y, x] == 0:
            intensity_diff = abs(int(gray[y, x]) - int(seed_intensity))
            if intensity_diff <= threshold:
                mask[y, x] = 255

                # Adiciona vizinhos à fila
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and mask[ny, nx] == 0:
                        queue.append((nx, ny))

    return mask


def apply_mask_on_image(image, mask):
    """
    Aplica a máscara segmentada sobre a imagem original,
    deixando a parte segmentada colorida e o restante em preto e branco.

    Parâmetros:
    - image: Imagem original em RGB
    - mask: Máscara da segmentação

    Retorna:
    - result: Imagem com área segmentada colorida e o restante em tons de cinza
    """
    # Converte imagem para escala de cinza
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)

    # Cria uma máscara booleana
    mask_bool = mask == 255

    # Aplica a máscara: área segmentada mantém as cores
    result = np.where(mask_bool[:, :, None], image, gray_image)

    return result


def region_based(image_path, seed_point, threshold=10):
    """
    Função de Region Growing adaptada para projeto Flask.

    Parâmetros:
    - image_path: Caminho para a imagem enviada pelo usuário
    - seed_point: Tupla (x, y) indicando o ponto semente
    - threshold: Limiar de diferença de intensidade para crescimento

    Retorna:
    - segmented_filenames: Dicionário com os nomes dos arquivos segmentados
    """

    # Lê a imagem
    image = cv2.imread(image_path)

    if image is None:
        return {}

    # Executa o algoritmo de Region Growing
    segmented_mask = region_growing(image, seed_point, threshold)

    # Aplica a máscara para obter a imagem destacada
    highlighted_image = apply_mask_on_image(image, segmented_mask)

    # Diretório de saída definido no Flask
    processed_folder = current_app.config['PROCESSED_FOLDER']
    os.makedirs(processed_folder, exist_ok=True)

    # Gera nomes de arquivos
    base_filename = os.path.basename(image_path)
    mask_filename = f"region_growing_mask_{base_filename}"
    highlighted_filename = f"region_growing_highlighted_{base_filename}"

    # Salva os arquivos
    mask_path = os.path.join(processed_folder, mask_filename)
    highlighted_path = os.path.join(processed_folder, highlighted_filename)

    cv2.imwrite(mask_path, segmented_mask)
    cv2.imwrite(highlighted_path, highlighted_image)

    # Retorna os nomes dos arquivos
    segmented_filenames = {
        "Region Growing": mask_filename,
        "Region Growing - Destacado": highlighted_filename
    }

    return segmented_filenames


# ========== TESTE DO ALGORITMO ==========
if __name__ == "__main__":
    # Caminho da imagem
    img_path = "images/a.png"

    # Define o ponto semente manualmente
    seed_point = (180, 90)

    # Simula o contexto do Flask
    class MockApp:
        config = {"PROCESSED_FOLDER": "processed"}

    current_app = MockApp()

    # Executa a segmentação
    result_files = region_growing_flask(img_path, seed_point, threshold=15)

    # Exibe os caminhos dos arquivos gerados
    for title, filename in result_files.items():
        print(f"{title}: {filename}")
