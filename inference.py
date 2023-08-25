# model inference API
from utils import *
import boto3

def handler(event, context):
    # Load model

    # load model from s3
    # s3 = boto3.client('s3', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)

    # bucket_name = 's3://bucket-plugissue'
    # object_key = 'model.pt'

    # response = s3.get_object(Bucket=bucket_name, Key=object_key)
    # data = response['Body'].read()

    # # save model to local
    # with open('./model.pt', 'wb') as file:
    #     file.write(data)

    # load model from local
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