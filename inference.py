# model inference API
from utils import *

def handler(event, context):

    # Load model and optimizer
    model = load_model()
    
    # import input from database
    r_seq = db2Rseq()
    h_seq = db2Hseq(h_step = 4, pred_step = 6)
    t = dt2T(pred_step = 6)
    s_attrs, _ = db2S()

    # export output to database
    output = model(r_seq.float(), h_seq.float(), t.int(), s_attrs.float())
    return y2db(output)

