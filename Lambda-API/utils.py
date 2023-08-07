# transform json to model's input
import json
import torch

def json_to_tensor(json_data):
    X = []
    for key in json_data.keys():
        X.append(list(json_data[key].values()))

    return torch.tensor(X)

def tensor_to_json(outputs):
    dict = {}
    for idx, output in enumerate(outputs):
        dict[idx] = int(output)
    
    return json.dumps(dict)