# model inference API
import torch
from utils import get_dt, json2tensor, tensor2json, selectXjson, updateYjson

def handler(event, context):
    """
    event = {}
    """
    time = get_dt()
    model = torch.jit.load('model.pt')
    X_base, X_embed, seq = selectXjson(time)
    sids, inputs =  json2tensor(event)
    outputs = model(inputs)

    return tensor2json(sids, outputs)

