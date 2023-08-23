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
    now = db2Now()
    outputs = torch.hstack([now, res_20, res_40, res_60, res_120])

    try:
        y2db(outputs) 
        return {'status':'Success', 'time': f'{get_now()}'}

    except: return {'status':'Failed'}

# def handler(event, context):
#     # Load model
#     model = torch.jit.load('model.pt')
    
#     # import input from database
#     r_seq = db2Rseq()
#     h_seq = db2Hseq(h_step = 4)
#     t = dt2T()
#     s_attrs, _ = db2S()

#     # model inference
#     minutes = [20, 40, 60, 120]
#     labels = [0, 1, 2]
#     for i, m in enumerate(minutes):
#         for j in labels:
#             # globals()[f'res_{m}'] = model(r_seq.float(), h_seq[:, i, :, :].float(), t[:, i, :].int(), s_attrs.float())
#             globals()[f'res{m}_{j}'] = model(r_seq.float(), h_seq[:, j, :, :].float(), t[:, j, :].int(), s_attrs.float())

#     # export output to database
#     now = db2Now()
#     outputs = torch.hstack([now] + [globals()[f'res{m}_{j}'] for j in labels for m in minutes])
#     return outputs
#     # print(outputs.shape)
#     # try:
#     #     y2db(outputs) 
#     #     return {'status':'Success', 'time': f'{get_now()}'}

#     # except: return {'status':'Failed'}