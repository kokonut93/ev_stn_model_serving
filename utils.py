from datetime import datetime
import json
import torch

def get_dt():
    now = datetime.now()
    dt = datetime(now.year, now.month, now.day, now.hour, now.minute//20*20, 00)
    dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    return dt

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