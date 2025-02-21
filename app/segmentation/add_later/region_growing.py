# VALOR THRESHOLD
# Imagens com baixo contraste	5 - 15	Segmentação mais restrita e precisa
# Imagens com médio contraste	15 - 30	Região cresce de forma equilibrada
# Imagens com alto contraste	30 - 60	Região mais expansiva
# Imagens com ruído	< 20 (pós filtro)	Evita inclusão de ruídos indesejados

import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import deque


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


# ========== TESTE DO ALGORITMO ==========
if __name__ == "__main__":
    # Carrega a imagem
    img_path = "images/cerebro.png"  # Substitua pelo caminho da sua imagem
    image = cv2.imread(img_path)

    # Defina o ponto semente manualmente (ex.: (x, y))
    seed_point = (59, 28)  # Altere para o ponto desejado

    # Aplica o algoritmo
    segmented = region_growing(image, seed_point, threshold=20)

    # Exibe os resultados
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.title("Imagem Original")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Segmentação - Region Growing")
    plt.imshow(segmented, cmap="gray")
    plt.axis("off")

    plt.show()
