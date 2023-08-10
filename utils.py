# transform json to model's input
import json
import torch

def json_to_tensor(json_data):
    X = []
    sids = list(json_data.keys())
    for sid in sids:
        X.append(list(json_data[sid].values()))

    return sids, torch.tensor(X)

def tensor_to_json(sids, outputs):
    dict = {}
    for idx in range(len(outputs)):
        dict[sids[idx]] = int(outputs[idx].argmax())
    
    return json.dumps(dict)