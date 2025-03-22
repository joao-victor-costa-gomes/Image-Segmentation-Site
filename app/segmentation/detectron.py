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
from detectron2.structures import Instances

# from detectron2.projects import point_rend

import os
import cv2 
import numpy
import torch
from flask import current_app
from collections import defaultdict
import time

# ---------- FUNÇÕES IMPORTANTES ----------

def clone_instances(instances):
    from detectron2.structures import Instances
    new_instances = Instances(instances.image_size)
    for k, v in instances.get_fields().items():
        new_instances.set(k, v.clone() if hasattr(v, 'clone') else v)
    return new_instances

def gerar_resumo_segmentacao(instances, metadata, image_shape):
    """
    Gera resumo da segmentação de instâncias com contagem por classe, área, caixas e confiança.

    Parâmetros:
    - instances: objeto Instances do Detectron2.
    - metadata: metadados do dataset (ex: MetadataCatalog).
    - image_shape: shape da imagem original (altura, largura, canais).

    Retorna:
    - dicionário com resumo de classes, áreas, instâncias e porcentagens.
    """
    data_summary = {
        "classes_detectadas": defaultdict(int),
        "area_por_classe": defaultdict(int),
        "instancias": []
    }

    class_names = metadata.get("thing_classes", [])
    masks = instances.pred_masks if instances.has("pred_masks") else None
    boxes = instances.pred_boxes if instances.has("pred_boxes") else None
    scores = instances.scores.tolist()
    pred_classes = instances.pred_classes.tolist()

    for idx, cls_id in enumerate(pred_classes):
        cls_name = class_names[cls_id] if cls_id < len(class_names) else str(cls_id)
        data_summary["classes_detectadas"][cls_name] += 1

        # Área da máscara
        area = int(masks[idx].sum()) if masks is not None else 0
        data_summary["area_por_classe"][cls_name] += area

        # Bounding box
        bbox = boxes[idx].tensor.tolist()[0] if boxes is not None else None

        # Adiciona dados da instância
        data_summary["instancias"].append({
            "classe": cls_name,
            "confiança": round(scores[idx], 3),
            "área_pixels": area,
            "bbox": bbox
        })

    # Calcular porcentagem de área (baseado no total da imagem)
    total_pixels = image_shape[0] * image_shape[1]
    for cls, area in data_summary["area_por_classe"].items():
        perc = round((area / total_pixels) * 100, 2)
        data_summary["area_por_classe"][cls] = f"{area} px ({perc}%)"

    return data_summary

# ---------- CRIAÇÃO DO DETECTOR ----------

# Criando uma classe para nosso detector
class Detector:

    def __init__(self, model_type=None, confidence_threshold=0.7, device=None):
        # Atributo que representa as configurações do nosso detector
        self.cfg = get_cfg()
        self.model_type = model_type
        self.filename = None
        self.segmentation_name = None

        # Object Detection
        if model_type == "OD": 
            # Carrega configurações de um modelo de segmentação treinado no conjunto de dados COCO
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))
            # Define o caminho para os pesos pretreinados do modelo treinado no conjunto de dados COCO
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")
            
            self.filename = "object_detection_"
            self.segmentation_name = "Detecção de Objetos"
        
        # Instance Segmentation
        elif model_type == "IS":
        # Carrega configurações de um modelo de segmentação treinado no conjunto de dados COCO
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
            # Define o caminho para os pesos pretreinados do modelo treinado no conjunto de dados COCO
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
            
            self.filename = "instance_segmentation_"
            self.segmentation_name = "Segmentação de Instâncias"

        # Panoptic Segmentation
        elif model_type == "PS":
            # Carrega configurações de um modelo de segmentação treinado no conjunto de dados COCO
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml"))
            # Define o caminho para os pesos pretreinados do modelo treinado no conjunto de dados COCO
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml")
            
            self.filename = "panoptic_segmentation_"
            self.segmentation_name = "Segmentação Panóptica"

        # Define o limiar de confiança mínimo para cada detecção (70% ou mais)
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8
        # Define o dispositivo em que o modelo será executado
        self.cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

        # Cria um objeto predictor e aplica as configurações
        self.predictor = DefaultPredictor(self.cfg)

    def segmentar_imagem(self, image_path):

        start_time = time.time() # INICIAR CONTADOR

        # Lê uma imagem
        image = cv2.imread(image_path)

        # Criar a pasta para salvar os arquivos processados
        processed_folder = current_app.config['PROCESSED_FOLDER']
        os.makedirs(processed_folder, exist_ok=True)
        base_name = os.path.basename(image_path)

        segmented_filenames = {}
        data_summary = {}

        # SEGMENTAÇÃO DE INSTÂNCIAS
        if self.model_type != "PS":
            # Realiza a predição
            predictions = self.predictor(image)
            instances = predictions["instances"].to("cpu")
            metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0])
            img_rgb = image[:, :, ::-1]

            # Cálculo de dados da segmentação
            data_summary = gerar_resumo_segmentacao(instances, metadata, image.shape)

            # Máscara + Caixas
            v_all = Visualizer(img_rgb=img_rgb.copy(), metadata=metadata)
            output_all = v_all.draw_instance_predictions(instances)
            image_all = output_all.get_image()[:, :, ::-1]
            # Salvando a imagem segmentada
            filename_all = f"{self.filename}{base_name}"
            cv2.imwrite(os.path.join(processed_folder, filename_all), image_all)
            segmented_filenames[f"{self.segmentation_name} (Máscara + Caixas)"] = filename_all

            # Só Máscaras
            instances_masks_only = clone_instances(instances)
            if "pred_boxes" in instances_masks_only.get_fields():
                instances_masks_only.remove("pred_boxes")
            v_masks = Visualizer(img_rgb=img_rgb.copy(), metadata=metadata)
            output_masks = v_masks.draw_instance_predictions(instances_masks_only)
            image_masks = output_masks.get_image()[:, :, ::-1]
            # Salvando a imagem segmentada
            filename_masks = f"{self.filename}masks_{base_name}"
            cv2.imwrite(os.path.join(processed_folder, filename_masks), image_masks)
            segmented_filenames[f"{self.segmentation_name} (Só Máscara)"] = filename_masks

            # Só Caixas
            instances_boxes_only = clone_instances(instances)
            if "pred_masks" in instances_boxes_only.get_fields():
                instances_boxes_only.remove("pred_masks")
            v_boxes = Visualizer(img_rgb=img_rgb.copy(), metadata=metadata)
            output_boxes = v_boxes.draw_instance_predictions(instances_boxes_only)
            image_boxes = output_boxes.get_image()[:, :, ::-1]
            # Salvando a imagem segmentada
            filename_boxes = f"{self.filename}boxes_{base_name}"
            cv2.imwrite(os.path.join(processed_folder, filename_boxes), image_boxes)
            segmented_filenames[f"{self.segmentation_name} (Só Caixas)"] = filename_boxes

        # SEGMENTAÇÃO PANÓPTICA
        else:
            # Realiza a predição
            predictions, segmentation_info = self.predictor(image)["panoptic_seg"]
            metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0])
            v = Visualizer(img_rgb=image[:, :, ::-1], metadata=metadata)
            output = v.draw_panoptic_seg_predictions(predictions.to("cpu"), segmentation_info)
            segmented_image = output.get_image()[:, :, ::-1]
            filename_all = f"{self.filename}{base_name}"
            cv2.imwrite(os.path.join(processed_folder, filename_all), segmented_image)
            segmented_filenames[f"{self.segmentation_name}"] = filename_all

        processing_time = round(time.time() - start_time, 3) # FINALIZAR CONTADOR




        print("\n\n=== Arquivos Segmentados ===")
        for nome, caminho in segmented_filenames.items():
            print(f"{nome}: {caminho}")

        print("\n=== Dados da Segmentação ===")
        for chave, valor in data_summary.items():
            print(f"{chave}:")
            print(valor)

        print("\n=== Tempo de Processamento ===")
        print(f"{processing_time} segundos\n\n")




        return {
            "arquivos_segmentados": segmented_filenames,
            "dados_segmentacao": data_summary,
            "tempo_processamento_segundos": processing_time
        }
