import os
import json
import torch
from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request


app = Flask(__name__)
imagenet_class_index = json.load(open('imagenet_class_index.json'))
model = torch.jit.load('model.pt')


def preprocess(img_path = "img_129.jpg"):
    img = Image.open(img_path).convert('L')
    transform = transforms.Compose([transforms.Grayscale(), transforms.ToTensor()])
    return transform(img).unsqueeze(0)


def get_prediction(image_path):
    tensor = preprocess(image_path)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        image_path = file.read()
        class_id, class_name = get_prediction(image_path=image_path)
        return jsonify({'class_id': class_id, 'class_name': class_name})


if __name__ == '__main__':
    app.run()