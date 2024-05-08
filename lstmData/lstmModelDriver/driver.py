import numpy as np

import torch
from torch.utils.data import DataLoader

from .download_data import download_data
from .data_normalization import Normalizer
from .data_prep import prepare_data_x, prepare_data_y
from .download_data_pytorch import TimeSeriesDataset

from .epoch import Epoch

print("All dependencies installed")

class Driver:
        
    # batta bing batta boom
    def get_price(updatedConfigs):

        # get lstm configurations based on inputted stock
        configs = updatedConfigs

        e = Epoch(configs)
        
        data_close_price = download_data(configs)[1]

        # Normalize

        scaler = Normalizer()
        normalized_data_close_price = scaler.fit_transform(data_close_price)

        # Prep data

        data_x, data_x_unseen = prepare_data_x(normalized_data_close_price, window_size=configs["data"]["window_size"])
        data_y = prepare_data_y(normalized_data_close_price, window_size=configs["data"]["window_size"])

        # Split dataset

        split_index = int(data_y.shape[0]*configs["data"]["train_split_size"])
        data_x_train = data_x[:split_index]
        data_x_val = data_x[split_index:]
        data_y_train = data_y[:split_index]
        data_y_val = data_y[split_index:]

        # training

        dataset_train = TimeSeriesDataset(data_x_train, data_y_train)
        dataset_val = TimeSeriesDataset(data_x_val, data_y_val)

        print("Train data shape", dataset_train.x.shape, dataset_train.y.shape)
        print("Validation data shape", dataset_val.x.shape, dataset_val.y.shape)

        train_dataloader = DataLoader(dataset_train, batch_size=configs["training"]["batch_size"], shuffle=True)
        val_dataloader = DataLoader(dataset_val, batch_size=configs["training"]["batch_size"], shuffle=True)

        # defining

        train_dataloader = DataLoader(dataset_train, batch_size=configs["training"]["batch_size"], shuffle=True)
        val_dataloader = DataLoader(dataset_val, batch_size=configs["training"]["batch_size"], shuffle=True)

        for epoch in range(configs["training"]["num_epoch"]):
            loss_train, lr_train = e.run_epoch(train_dataloader, is_training=True)
            loss_val, lr_val = e.run_epoch(val_dataloader)
            e.scheduler.step()
            
            print('Epoch[{}/{}] | loss train:{:.6f}, test:{:.6f} | lr:{:.6f}'
                    .format(epoch + 1, configs["training"]["num_epoch"], loss_train, loss_val, lr_train))
            

        # re-initialize dataloader so the data doesn't shuffled, so we can plot the values by date

        train_dataloader = DataLoader(dataset_train, batch_size=configs["training"]["batch_size"], shuffle=False)
        val_dataloader = DataLoader(dataset_val, batch_size=configs["training"]["batch_size"], shuffle=False)

        e.model.eval()

        # predict on the training data, to see how well the model managed to learn and memorize

        predicted_train = np.array([])

        for idx, (x, y) in enumerate(train_dataloader):
            x = x.to(configs["training"]["device"])
            out = e.model(x)
            out = out.cpu().detach().numpy()
            predicted_train = np.concatenate((predicted_train, out))

        # predict on the validation data, to see how the model does

        predicted_val = np.array([])

        for idx, (x, y) in enumerate(val_dataloader):
            x = x.to(configs["training"]["device"])
            out = e.model(x)
            out = out.cpu().detach().numpy()
            predicted_val = np.concatenate((predicted_val, out))

        # predict the closing price of the next trading day

        e.model.eval()

        x = torch.tensor(data_x_unseen).float().to(configs["training"]["device"]).unsqueeze(0).unsqueeze(2) # this is the data type and shape required, [batch, sequence, feature]
        prediction = e.model(x)
        prediction = prediction.cpu().detach().numpy()

        plot_range = 10
        final_prediction = np.zeros(plot_range)


        final_prediction[plot_range-1] = scaler.inverse_transform(prediction)
        final_prediction = np.where(final_prediction == 0, None, final_prediction)

        
        return round(final_prediction[plot_range-1], 2)
