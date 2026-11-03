from huggingface_hub import hf_hub_download
from ultralytics import YOLO

weights = hf_hub_download("Ank0805/waste-classification", "waste classification modle.pt")
model = YOLO(weights)
source = 'http://images.cocodataset.org/val2017/000000039769.jpg'
model.predict(source=source, save=True)
