# model inference API
import torch
from utils import db2Rseq, db2Hseq, dt2T, db2S, y2db

def handler(event, context):
    """
    event = {model.pt}
    """

    # import input from database
    r_seq = db2Rseq()
    h_seq = db2Hseq()
    t = dt2T()
    s = db2S()

    # export output to database
    model = torch.jit.load('model.pt')
    outputs = model(r_seq, h_seq, t, s)
    
    return y2db(outputs)

