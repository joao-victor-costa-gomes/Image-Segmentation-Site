import cv2
import matplotlib.pyplot as plt
import numpy as np

# Lê a imagem
image = cv2.imread('coins1.png')

# Converte a imagem de BGR para RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Converte para escala de cinza
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Verifica se o fundo é claro e inverte a imagem se necessário
if np.mean(gray) > 127:
    gray = cv2.bitwise_not(gray)  # Inverte a imagem para destacar os objetos

# Remove ruídos com filtro Gaussiano
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Aplica limiarização de Otsu
_, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Remove pequenos ruídos (morphological opening)
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)


# Define o fundo certo (dilatação)
sure_bg = cv2.dilate(opening, kernel, iterations=3)

# Encontra o primeiro plano (objetos) usando a distância Euclidiana
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

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

# Marca os componentes conectados
ret, markers = cv2.connectedComponents(sure_fg)

# Ajusta os rótulos para que o fundo não seja 0
markers = markers + 1

# Define áreas desconhecidas como 0
markers[unknown == 255] = 0

# Cria uma cópia da imagem para desenhar as bordas
image_with_borders = image_rgb.copy()

# Aplica o algoritmo Watershed (apenas uma vez)
markers = cv2.watershed(image, markers)

# Marca as bordas em vermelho
image_with_borders[markers == -1] = [255, 0, 0]  # Bordas em vermelho

# Cria uma imagem colorida para visualização preenchida
segmented = np.zeros_like(image_rgb)
for marker in np.unique(markers):
    if marker == -1:
        segmented[markers == marker] = [255, 0, 0]  # Bordas em vermelho
    elif marker == 1:
        segmented[markers == marker] = [0, 0, 0]    # Fundo em preto
    else:
        color = np.random.randint(0, 255, size=3)   # Cores aleatórias
        segmented[markers == marker] = color

# Exibe as imagens finais
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
axes[0].imshow(image_with_borders)
axes[0].set_title("Watershed com Bordas")
axes[0].axis("off")

axes[1].imshow(segmented)
axes[1].set_title("Watershed Preenchido")
axes[1].axis("off")

plt.show()
