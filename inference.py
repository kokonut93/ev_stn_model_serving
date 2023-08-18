# model inference API
import torch
from model import MultiSeqBase
from utils import db2Rseq, db2Hseq, dt2T, db2S, y2db




def handler(event, context):
    """
    event = {model.pt}
    """

    # Load model and optimizer
    model = MultiSeqBase(n_labels=3, hidden_size=32, embedding_dim=4, dropout_p=0.2)
    optim = torch.optim.Adam(model.parameters(), weight_decay=1e-3)

    checkpoint = torch.load('test_model_and_optimizer.pth')
    model.load_state_dict(checkpoint['model_state_dict'])
    optim.load_state_dict(checkpoint['optimizer_state_dict'])

    
    # import input from database
    r_seq = db2Rseq()
    h_seq = db2Hseq()
    t = dt2T()
    s_attrs, _ = db2S()

    # export output to database
    output = model(r_seq.float(), h_seq.float(), t.int(), s_attrs.float()).argmax(dim=1)    
    return y2db(output)

