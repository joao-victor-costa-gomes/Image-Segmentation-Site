# https://www.youtube.com/watch?v=MuzNooUNZSY

# ---------- IMPORTAÇÕES ----------

# Biblioteca de aprendizado profundo 
import torch
# Biblioteca para detecção de objetos
import detectron2

# Trabalha com grandes matrizes e matrizes multidimensionais (matriz da imagem)
import numpy as np 
# Processamento de imagens e vídeos
import cv2
# Para plotar as imagens
import matplotlib.pyplot as plt

# Carrega modelos pretreinados
from detectron2 import model_zoo
# Facilita a inferência usando um modelo pretreinado com configuração padrão
from detectron2.engine import DefaultPredictor
# Para carregar e configurar as definições do modelo
from detectron2.config import get_cfg
# Classe que ajuda a visualizar os resultados das previsões do modelo
from detectron2.utils.visualizer import Visualizer
# Gerencia informações de metadados sobre conjuntos de dados usados no Detectron2, como nomes de classes e cores
from detectron2.data import MetadataCatalog

# ---------- IMPLEMENTAÇÃO ----------

# Carregando imagem 
image_path = "imagens/garota_e_cachorro.jpg"
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Cria um objeto de configuração para definir várias opções do modelo e do processo de inferência
cfg = get_cfg()
# Carrega configurações de um modelo de segmentação treinado no conjunto de dados COCO
cfg.merge_from_file(model_zoo.get_config_file("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml"))
# Define o caminho para os pesos pretreinados do modelo treinado no conjunto de dados COCO
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml")
# Define o dispositivo em que o modelo será executado
cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Cria um objeto predictor, ele facilita a aplicação de um modelo pretreinado para fazer previsões em novas imagens
predictor = DefaultPredictor(cfg)
# Aplica o modelo à imagem image_rgb
# ["panoptic_seg"] extrai a segmentação panóptica e informações de segmentação associadas
panoptic_segmentation, segmentation_info = predictor(image_rgb)["panoptic_seg"]

# Cria um objeto Visualizer que facilita a visualização dos resultados da segmentação
# image_rgb[:, :, ::-1] converte a imagem de volta para o formato BGR
# MetadataCatalog.get(cfg.DATASETS.TRAIN[0]) obtém os metadados relevantes (como nomes de classes e cores) do conjunto de dados usado para treinar o modelo.
# scale no Visualizer controla o fator de escala da imagem durante a visualização (1.0 = tamanho original)
v = Visualizer(image_rgb[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.0)

# Desenha as previsões de segmentação panóptica na imagem original.
out = v.draw_panoptic_seg_predictions(panoptic_segmentation.to("cpu"), segmentation_info)
# Extrai a imagem segmentada do objeto out, convertendo-a de volta para o formato RGB
segmented_image = out.get_image()[:, :, ::-1]

# Mostra a imagem segmentada
plt.figure(figsize=(10, 10))
plt.imshow(segmented_image)
plt.axis("off")
plt.show()
