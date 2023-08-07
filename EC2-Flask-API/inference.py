import io
import torch
from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request


app = Flask(__name__)
model = torch.jit.load('model.pt')


def preprocess(file):
    # with open(file, 'rb') as f:
    #     img_path = f.read()
    img_path = file.read()
    img = Image.open(io.BytesIO(img_path))
    transform = transforms.Compose([transforms.Grayscale(), transforms.ToTensor()])
    return transform(img).unsqueeze(0)


def get_inference(file):
    tensor = preprocess(file)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_class = str(y_hat.item())
    return predicted_class

@app.route('/')
def index():
    if request.method == 'GET':
        return 'index'


@app.route('/inference', methods=['POST'])
<<<<<<< HEAD:inference.py
def predict():
=======
def inference():
>>>>>>> dfbb6b7d84f718e28ccadb2b5c21585a1eee0349:EC2-Flask-API/inference.py
    if request.method == 'POST':
        file = request.files['file']
        evcs_class = get_inference(file = file)
        return jsonify({'evcs_class': evcs_class})


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)