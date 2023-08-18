import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class MultiSeqBase(nn.Module):
    def __init__(self, n_labels, hidden_size, embedding_dim, dropout_p):
        super().__init__()
        self.lstm_r1 = nn.LSTM(1, hidden_size, 1, batch_first=True)
        self.fc_r1 = nn.Linear(hidden_size, 16)
    
        self.lstm_h1 = nn.LSTM(1, hidden_size, 1, batch_first=True)
        self.fc_h1 = nn.Linear(hidden_size, 16)

        self.timeslot_embedding = nn.Embedding(num_embeddings=144, embedding_dim=embedding_dim)
        self.dow_embedding = nn.Embedding(num_embeddings=7, embedding_dim=embedding_dim)
        self.we_embedding = nn.Embedding(num_embeddings=2, embedding_dim=embedding_dim)

        self.fc_b1 = nn.Linear(3*embedding_dim, 128)
        self.fc_b2 = nn.Linear(128, 128)
        self.fc_b3 = nn.Linear(128, 64)

        self.fc_cat = nn.Linear(32+64, 64)
        self.top = nn.Linear(64,n_labels)
        self.dropout = nn.Dropout(p=dropout_p)

    def forward(self, r, h, t, s):
        # realtime sequence
        lstm_out_r, (hn, cn) = self.lstm_r1(r)
        last_state_r = lstm_out_r[:,-1,:]
        realtime_vec = self.dropout(last_state_r)
        realtime_vec = F.relu(self.fc_r1(realtime_vec))
        
        # history sequence
        lstm_out_h, (hn, cn) = self.lstm_h1(h)
        last_state_h = lstm_out_h[:,-1,:]
        history_vec = self.dropout(last_state_h)
        history_vec = F.relu(self.fc_h1(history_vec))

        # non-sequenctials
        timeslot_vec = self.timeslot_embedding(t[:,0])
        dow_vec = self.dow_embedding(t[:,1])
        we_vec = self.we_embedding(t[:,2])

        fc_in = torch.cat((timeslot_vec, dow_vec, we_vec), dim=1)
        feature_vec = F.relu(self.fc_b1(fc_in))
        feature_vec = F.relu(self.fc_b2(feature_vec))
        feature_vec = F.relu(self.fc_b3(feature_vec))

        # concatenation
        cat_vec = torch.cat((realtime_vec, history_vec, feature_vec), dim=1)
        fc_out = F.relu(self.fc_cat(cat_vec))
        fc_out = self.dropout(fc_out)
        fc_out = self.top(fc_out)
        return torch.sigmoid(fc_out)
