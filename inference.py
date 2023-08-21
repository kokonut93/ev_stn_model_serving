# model inference API
from utils import *

def handler(event, context):

    # Load model
    model = torch.jit.load('model.pt')
    
    # import input from database
    r_seq = db2Rseq()
    h_seq = db2Hseq(h_step = 4)
    t = dt2T()
    s_attrs, _ = db2S()

    # model inference
    minutes = [20, 40, 60, 120]

    for i, m in enumerate(minutes):
        globals()[f'res_{m}'] = model(r_seq.float(), h_seq[:, i, :, :].float(), t[:, i, :].int(), s_attrs.float())

    # export output to database
    outputs = torch.hstack([res_20, res_40, res_60, res_120])

    try:
        y2db(outputs) 
        return {'status':'Success', 'time': f'{get_now()}'}

    except: return {'status':'Failed'}
