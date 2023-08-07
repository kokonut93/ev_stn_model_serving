import io
import torch
from torchvision import models
import torchvision.transforms as transforms
from PIL import Image


def preprocess(file):
    # with open(file, 'rb') as f:
    #     img_path = f.read()
    img_path = file.read()
    img = Image.open(io.BytesIO(img_path))
    transform = transforms.Compose([transforms.Grayscale(), transforms.ToTensor()])
    return transform(img).unsqueeze(0)


def get_prediction(file):
    tensor = preprocess(file)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_class = str(y_hat.item())
    return predicted_class


evcs_class = get_prediction(file = file)


def handler(event, context):
    event[]