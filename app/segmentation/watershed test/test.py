import cv2
import matplotlib.pyplot as plt
import numpy as np

def watershed_segmentation(image_path, limiar_inversao=127, kernel_gaussiano=7, usar_otsu=True, limiar_manual=128,
                            kernel_morfologico=3, limiar_dist_transform=0.5,
                            iteracoes_dilatacao=3, iteracoes_erosao=2):
    # Lê a imagem
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Converte para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Se o fundo for claro, inverter a imagem
    if np.mean(gray) > limiar_inversao:
        gray = cv2.bitwise_not(gray)
    
    # Aplicar filtro Gaussiano para suavizar ruídos
    blur = cv2.GaussianBlur(gray, (kernel_gaussiano, kernel_gaussiano), 0)
    
    # Aplica limiarização de Otsu ou limiar manual
    if usar_otsu:
        _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        _, binary = cv2.threshold(blur, limiar_manual, 255, cv2.THRESH_BINARY)
    
    # Remover pequenos ruídos com "closing" para fechar buracos
    kernel = np.ones((kernel_morfologico, kernel_morfologico), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # Determinar o fundo certo (dilatação)
    sure_bg = cv2.dilate(cleaned, kernel, iterations=iteracoes_dilatacao)
    
    # Encontrar os objetos no primeiro plano usando a transformada de distância
    dist_transform = cv2.distanceTransform(cleaned, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, limiar_dist_transform * dist_transform.max(), 255, 0)
    
    # Definir áreas desconhecidas
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # Criar marcadores para Watershed
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1  # Evita que o fundo seja 0
    markers[unknown == 255] = 0  # Define a área desconhecida como 0
    
    # Aplicar Watershed
    cv2.watershed(image, markers)
    
    # Criar imagem segmentada colorida
    segmented = np.zeros_like(image_rgb)
    for marker in np.unique(markers):
        if marker == -1:
            segmented[markers == marker] = [255, 0, 0]  # Bordas em vermelho
        elif marker == 1:
            segmented[markers == marker] = [0, 0, 0]    # Fundo em preto
        else:
            color = np.random.randint(0, 255, size=3)   # Cores aleatórias
            segmented[markers == marker] = color
    
    # Exibir resultados
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    axes[0].imshow(image_rgb)
    axes[0].set_title("Imagem Original")
    axes[0].axis("off")
    
    axes[1].imshow(segmented)
    axes[1].set_title("Segmentação Watershed")
    axes[1].axis("off")
    
    plt.show()
    
    return segmented
