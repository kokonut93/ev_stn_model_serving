# model inference API
from utils import *
import boto3

def handler(event, context):
    # Load model

    # load model from s3
    # s3 = boto3.client('s3')
    # bucket_name = 'your_bucket_name'
    # object_key = 'your_object_key'

    # response = s3.get_object(Bucket=bucket_name, Key=object_key)
    # data = response['Body'].read()

    # save model to local
    # with open('/tmp/model.pt', 'wb') as file:
    #     file.write(data)

    # load model from local
    # model = torch.jit.load('/tmp/model.pt')
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


# import boto3

# def lambda_handler(event, context):
#     s3 = boto3.client('s3')
#     bucket_name = 'your_bucket_name'
#     object_key = 'your_object_key'

#     response = s3.get_object(Bucket=bucket_name, Key=object_key)
#     data = response['Body'].read()

#     # 로컬에 파일로 저장
#     with open('/tmp/model.pt', 'wb') as file:
#         file.write(data)

#     # PyTorch에서 모델 로드
#     model = torch.jit.load('/tmp/model.pt')

