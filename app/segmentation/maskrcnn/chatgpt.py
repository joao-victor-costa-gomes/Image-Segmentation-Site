import cv2
import numpy as np
import torch
import matplotlib.pyplot as plt
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

def setup_mask_rcnn():
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # Define um limiar de confiança para detecção
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # Usa GPU se disponível
    return DefaultPredictor(cfg)

def segment_image(image_path, predictor):
    # Carrega a imagem
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Faz a previsão com Mask R-CNN
    outputs = predictor(image_rgb)

    # Visualiza os resultados
    v = Visualizer(image_rgb[:, :, ::-1], MetadataCatalog.get("coco_2017_train"), scale=1.2)
    v = v.draw_instance_predictions(outputs["instances"].to("cpu"))

    # Exibe a imagem segmentada
    plt.figure(figsize=(10, 10))
    plt.imshow(v.get_image())
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    predictor = setup_mask_rcnn()
    image_path = "pedestres02.jpg"  
    segment_image(image_path, predictor)