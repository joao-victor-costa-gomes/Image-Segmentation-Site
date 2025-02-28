import os
import cv2
import numpy as np
from flask import current_app

def watershed_segmentation(image_path, 
        limiar_inversao=127, 
        kernel_gaussiano=7, 
        usar_otsu=True, 
        limiar_manual=128, 
        kernel_morfologico=3, 
        limiar_dist_transform=0.5,
        iteracoes_dilatacao=3, 
        iteracoes_erosao=2
    ):
    
    image = cv2.imread(image_path)
    
    if image is None:
        return {}
    
    # Converter para RGB imediatamente
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Criar a pasta para salvar os arquivos processados
    processed_folder = current_app.config['PROCESSED_FOLDER']
    os.makedirs(processed_folder, exist_ok=True)
    
    segmented_filenames = {}
    
    # Converte para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
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
    
    binary_filename = f"binary_{os.path.basename(image_path)}"
    cv2.imwrite(os.path.join(processed_folder, binary_filename), binary)
    segmented_filenames["Imagem Binarizada"] = binary_filename
    
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
    
    # Criar imagem segmentada com bordas
    image_with_borders = image.copy()
    # image_with_borders[markers == -1] = [0, 0, 255]  # Bordas em vermelho (já no formato RGB)

    # Criar uma máscara apenas para as bordas
    borders = (markers == -1).astype(np.uint8) * 255

    # Aumentar a grossura usando dilatação
    kernel = np.ones((2, 2), np.uint8)  # Ajuste o tamanho do kernel conforme necessário
    borders_thick = cv2.dilate(borders, kernel, iterations=1)

    # Aplicar as bordas grossas na imagem
    image_with_borders[borders_thick == 255] = [255, 0, 0]  # Vermelho

    # Imagem com as cores certas
    image_with_borders = cv2.cvtColor(image_with_borders, cv2.COLOR_BGR2RGB)
    
    borders_filename = f"watershed_borders_{os.path.basename(image_path)}"
    cv2.imwrite(os.path.join(processed_folder, borders_filename), image_with_borders)
    segmented_filenames["Segmentação Watershed (Bordas)"] = borders_filename
    
    # Criar imagem segmentada colorida preenchida
    segmented_filled = np.zeros_like(image)
    for marker in np.unique(markers):
        if marker == -1:
            segmented_filled[markers == marker] = [255, 0, 0]  # Bordas em vermelho
        elif marker == 1:
            segmented_filled[markers == marker] = [0, 0, 0]    # Fundo em preto
        else:
            color = np.random.randint(0, 255, size=3)   # Cores aleatórias
            segmented_filled[markers == marker] = color

    # Imagem com as cores certas
    segmented_filled = cv2.cvtColor(segmented_filled, cv2.COLOR_BGR2RGB)
    
    filled_filename = f"watershed_filled_{os.path.basename(image_path)}"
    cv2.imwrite(os.path.join(processed_folder, filled_filename), segmented_filled)
    segmented_filenames["Segmentação Watershed (Preenchida)"] = filled_filename
    
    return segmented_filenames
