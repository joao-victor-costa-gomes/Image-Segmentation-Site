import cv2
import matplotlib.pyplot as plt
import numpy as np

def watershed_segmentation(image_path, 
                           blur_kernel_size=(5, 5),
                           morph_kernel_size=(3, 3),
                           morph_iterations=2,
                           distance_threshold=0.7,
                           adaptive_threshold=False,
                           closing_operation=True,
                           dilate_iterations=3,
                           invert_background=True):
    """
    Função para segmentação de imagens usando o algoritmo Watershed.

    Parâmetros:
    - image_path (str): Caminho para a imagem.
    - blur_kernel_size (tuple): Tamanho do kernel para o filtro Gaussiano.
    - morph_kernel_size (tuple): Tamanho do kernel para operações morfológicas.
    - morph_iterations (int): Número de iterações para operações morfológicas.
    - distance_threshold (float): Fator para limiarização da transformada de distância.
    - adaptive_threshold (bool): Usa limiarização adaptativa se True, senão usa Otsu.
    - closing_operation (bool): Aplica fechamento (MORPH_CLOSE) se True, abertura se False.
    - dilate_iterations (int): Número de iterações na dilatação do fundo.
    - invert_background (bool): Inverte imagem se fundo for claro.
    """

    # Lê a imagem
    image = cv2.imread(image_path)

    # Converte a imagem de BGR para RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Converte para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Inverte fundo claro se necessário
    if invert_background and np.mean(gray) > 127:
        gray = cv2.bitwise_not(gray)

    # Remove ruídos com filtro Gaussiano
    blur = cv2.GaussianBlur(gray, blur_kernel_size, 0)

    # Limiarização adaptativa ou Otsu
    if adaptive_threshold:
        binary = cv2.adaptiveThreshold(blur, 255, 
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY_INV, 11, 2)
    else:
        _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Operações Morfológicas
    kernel = np.ones(morph_kernel_size, np.uint8)
    morph_type = cv2.MORPH_CLOSE if closing_operation else cv2.MORPH_OPEN
    morph = cv2.morphologyEx(binary, morph_type, kernel, iterations=morph_iterations)

    # Define o fundo certo (dilatação)
    sure_bg = cv2.dilate(morph, kernel, iterations=dilate_iterations)

    # Encontra o primeiro plano (objetos) usando a distância Euclidiana
    dist_transform = cv2.distanceTransform(morph, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, distance_threshold * dist_transform.max(), 255, 0)

    # Define áreas desconhecidas
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Exibe pré-processamento
    fig, axes = plt.subplots(2, 3, figsize=(18, 6))
    axes[0, 0].imshow(image_rgb)
    axes[0, 0].set_title("Imagem Original")
    axes[0, 0].axis("off")

    axes[0, 1].imshow(gray, cmap='gray')
    axes[0, 1].set_title("Escala de Cinza")
    axes[0, 1].axis("off")

    axes[0, 2].imshow(binary, cmap='gray')
    axes[0, 2].set_title("Imagem Binarizada")
    axes[0, 2].axis("off")

    axes[1, 0].imshow(sure_bg, cmap='gray')
    axes[1, 0].set_title("Fundo Certo")
    axes[1, 0].axis("off")

    axes[1, 1].imshow(dist_transform, cmap='gray')
    axes[1, 1].set_title("Transformada de Distância")
    axes[1, 1].axis("off")

    axes[1, 2].imshow(sure_fg, cmap='gray')
    axes[1, 2].set_title("Primeiro Plano Certo")
    axes[1, 2].axis("off")

    plt.tight_layout()
    plt.show()

    # Watershed
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    # Cópia da imagem para desenhar as bordas
    image_with_borders = image_rgb.copy()

    # Aplica o algoritmo Watershed
    markers = cv2.watershed(image, markers)

    # Marca as bordas em vermelho
    image_with_borders[markers == -1] = [255, 0, 0]

    # Cria uma imagem colorida para visualização preenchida
    segmented = np.zeros_like(image_rgb)
    for marker in np.unique(markers):
        if marker == -1:
            segmented[markers == marker] = [255, 0, 0]
        elif marker == 1:
            segmented[markers == marker] = [0, 0, 0]
        else:
            color = np.random.randint(0, 255, size=3)
            segmented[markers == marker] = color

    # Exibe os resultados finais
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    axes[0].imshow(image_with_borders)
    axes[0].set_title("Watershed com Bordas")
    axes[0].axis("off")

    axes[1].imshow(segmented)
    axes[1].set_title("Watershed Preenchido")
    axes[1].axis("off")

    plt.show()

# ===========================
# 🔥 USANDO A FUNÇÃO:
# ===========================

# Exemplo básico com parâmetros padrão
watershed_segmentation("coins2.png")

# Exemplo com parâmetros customizados
watershed_segmentation("caps.png", 
                       blur_kernel_size=(7, 7), 
                       morph_kernel_size=(5, 5), 
                       morph_iterations=3, 
                       distance_threshold=0.5, 
                       adaptive_threshold=True, 
                       closing_operation=False, 
                       dilate_iterations=4)
