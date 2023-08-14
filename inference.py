# model inference API
import torch
from utils import json2tensor, tensor2json, getXjson, updateYjson

def handler(event, context):
    """
    event = {
        "0": {
            "latitude": 39.7145,
            "longitude": 127.9425,
            ...
        },
    }
    """
    model = torch.jit.load('model.pt')
    sids, inputs =  json2tensor(event)
    outputs = model(inputs)

    return tensor2json(sids, outputs)

