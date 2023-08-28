# model inference API
from utils import *
import boto3

def handler(event, context):
    # Load model

    s3 = boto3.client('s3')

    models = []

    bucket_name = 'bucket-plugissue'
    pred_steps = [1, 2, 3, 6]

    for i in pred_steps:
        object_key = f'model_output/{i}/MultiSeqUmapEmb_epoch-100_pred_step-{i}_model.pt'
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        data = response['Body'].read()

        with open(f'./model_{i}.pt', 'wb') as file:
            file.write(data)

        models.append(torch.jit.load(f'/tmp/model_{i}.pt'))

    # Load input from database
    r_seq = db2Rseq()
    h_seq = db2Hseq(h_step = 4)
    t = dt2T()
    s_attrs, _ = db2S()

    # model inference
    for i, m in enumerate(pred_steps):
        globals()[f'res_{m}'] = models[i](r_seq.float(), h_seq[:, i, :, :].float(), t[:, i, :].int(), s_attrs.float())

    # export output to database
    now = db2Now()
    outputs = torch.hstack([now, res_1, res_2, res_3, res_6])

    try:
        y2db(outputs) 
        return {'status':'Success', 'time': f'{get_now()}'}

    except: return {'status':'Failed'}