import cv2
import matplotlib.pyplot as plt
import numpy as np

# Lê a imagem
image = cv2.imread('coins4.png')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Converte para escala de cinza
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Se o fundo for claro, inverter a imagem
if np.mean(gray) > 127:
    gray = cv2.bitwise_not(gray)

# Aplicar filtro Gaussiano para suavizar ruídos
blur = cv2.GaussianBlur(gray, (7, 7), 0)

# Aplica limiarização de Otsu
_, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Remover pequenos ruídos com "closing" para fechar buracos
kernel = np.ones((3, 3), np.uint8)
cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

# Determinar o fundo certo (dilatação)
sure_bg = cv2.dilate(cleaned, kernel, iterations=3)

# Encontrar os objetos no primeiro plano usando a transformada de distância
dist_transform = cv2.distanceTransform(cleaned, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)  # Reduzido para separar melhor

# Definir áreas desconhecidas
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
axes[0, 2].set_title("Imagem Binarizada (Otsu)")
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