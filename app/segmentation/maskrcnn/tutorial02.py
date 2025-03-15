# https://www.youtube.com/watch?v=Pb3opEFP94U&t=25s

# ---------- IMPORTAÇÕES ----------

# Para carregar e configurar as definições do modelo
from detectron2.config import get_cfg
# Facilita a inferência usando um modelo pretreinado com configuração padrão
from detectron2.engine import DefaultPredictor
# Gerencia informações de metadados sobre conjuntos de dados usados no Detectron2, como nomes de classes e cores
from detectron2.data import MetadataCatalog
# Carrega modelos pretreinados
from detectron2 import model_zoo
# Classe que ajuda a visualizar os resultados das previsões do modelo
from detectron2.utils.visualizer import Visualizer, ColorMode

import cv2 
import numpy
import torch

# ---------- CRIAÇÃO DO DETECTOR ----------

# Criando uma classe para nosso detector
class Detector:

    def __init__(self, model_type="OD"):
        # Atributo que representa as configurações do nosso detector
        self.cfg = get_cfg()
        self.model_type = model_type

        # Object Detection
        if model_type == "OD": 
            # Carrega configurações de um modelo de segmentação treinado no conjunto de dados COCO
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))
            # Define o caminho para os pesos pretreinados do modelo treinado no conjunto de dados COCO
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")
        
        # Instance Segmentation
        elif model_type == "IS":
        # Carrega configurações de um modelo de segmentação treinado no conjunto de dados COCO
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
            # Define o caminho para os pesos pretreinados do modelo treinado no conjunto de dados COCO
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")

        # Panoptic Segmentation
        elif model_type == "PS":
            # Carrega configurações de um modelo de segmentação treinado no conjunto de dados COCO
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml"))
            # Define o caminho para os pesos pretreinados do modelo treinado no conjunto de dados COCO
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml")

        # Define o limiar de confiança mínimo para cada detecção (70% ou mais)
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8
        # Define o dispositivo em que o modelo será executado
        self.cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

        # Cria um objeto predictor e aplica as configurações
        self.predictor = DefaultPredictor(self.cfg)

    def segmentar_imagem(self, image_path):
        # Lê uma imagem
        image = cv2.imread(image_path)

        if self.model_type != "PS":
            # Utiliza o objeto predictor, já configurado, na imagem
            predictions = self.predictor(image)
            # Cria um objeto Visualizer que facilita a visualização dos resultados da segmentação
            v = Visualizer(img_rgb=image[:, :, ::-1], metadata=MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]))
            # Desenha as predições do modelo na imagem usando o Visualizer
            # Esse tipo de visualizer só desenha uma caixinha em volta dos objetos
            output = v.draw_instance_predictions(predictions["instances"].to("cpu"))
        
        else:
            # Utiliza o objeto predictor, já configurado, na imagem
            predictions, segmentation_info = self.predictor(image)["panoptic_seg"]
            # Cria um objeto Visualizer que facilita a visualização dos resultados da segmentação
            v = Visualizer(img_rgb=image[:, :, ::-1], metadata=MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]))
            # Desenha as predições do modelo na imagem usando o Visualizer
            # Esse tipo de visualizer só desenha uma caixinha em volta dos objetos
            output = v.draw_panoptic_seg_predictions(predictions.to("cpu"), segmentation_info)

        cv2.imshow("Imagem Segmentada", output.get_image()[:, :, ::-1])
        cv2.waitKey(0)

# ---------- APLICAÇÃO DO DETECTOR ----------

segmentador = Detector(model_type="IS")

segmentador.segmentar_imagem("imagens/garota_e_cachorro.jpg")