import torch.optim as optim
import torch.nn as nn
from .config import Configurations
from .LSTMModel import LSTMModel


class Epoch:

    def __init__(self, configs):
        self.configs = configs
        self.model = LSTMModel(input_size=configs["model"]["input_size"], hidden_layer_size=configs["model"]["lstm_size"], num_layers=configs["model"]["num_lstm_layers"], output_size=1, dropout=configs["model"]["dropout"])
        self.model =self.model.to(configs["training"]["device"])
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=configs["training"]["learning_rate"], betas=(0.9, 0.98), eps=1e-9)
        self.scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=configs["training"]["scheduler_step_size"], gamma=0.1)

    def run_epoch(self, dataloader, is_training=False):

        epoch_loss = 0

        if is_training:
            self.model.train()
        else:
             self.model.eval()

        for idx, (x, y) in enumerate(dataloader):
            if is_training:
                 self.optimizer.zero_grad()

            batchsize = x.shape[0]

            x = x.to(self.configs["training"]["device"])
            y = y.to(self.configs["training"]["device"])

            out =  self.model(x)
            loss = self.criterion(out.contiguous(), y.contiguous())

            if is_training:
                loss.backward()
                self.optimizer.step()

            epoch_loss += (loss.detach().item() / batchsize)

        lr = self.scheduler.get_last_lr()[0]

        return epoch_loss, lr

