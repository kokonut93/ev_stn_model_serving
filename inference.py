# model inference API
import torch
from model import MultiSeqBase
from utils import *

def handler(event, context):
    """
    event = {model.pt}
    """

    # Load model and optimizer
    model = load_model()
    
    # import input from database
    r_seq = db2Rseq()
    h_seq = db2Hseq()
    t = dt2T()
    s_attrs, _ = db2S()

    # export output to database
    output = model(r_seq.float(), h_seq.float(), t.int(), s_attrs.float()).argmax(dim=1)    
    return y2db(output)

