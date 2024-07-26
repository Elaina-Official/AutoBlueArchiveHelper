import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from ultralytics import YOLO
import torch
from torch.utils.data import DataLoader

# 启用 cuda
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# 训练 yolov8 数据集
model = YOLO("yolov8n.yaml")
# 加载 yolov8 预训练模型(训练时)
# model = YOLO("yolov8n.pt")
# 加载预训练模型(推理时)
model = YOLO("../Datasets/best.pt")

if __name__ == '__main__':
    # 训练模型(训练时)
    # model.train(data="dataset.yaml", epochs=50)
    # 结果
    results = model.predict(source="", save=True, save_conf=True, save_txt=True, name="output")