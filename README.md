# REST API For Next Day Prices
Bi-layer LSTM model, enabling next-day price forecasting and providing outputs in JSON format upon request. *Can't be deployed at the moment due to the size of Pytorch's packages but a demonstration is provided below and feel free to use locally!*. 

For more information on the actual time-series LSTM see my other repository titled "predicting-day-stock-prices"

it runs over a hundred epochs on a fixed learning rate but adjust anything you think works better.
### Prerequisites:
Python3<br>
Django<br>

### Installation:
First, clone:
```
git clone https://github.com/Fadeleke57/bonsai-finance-app.git
cd bonsai-finance-app
```

Install Django Rest Framework, Django Depug Toolbar, and the dependencies for the model:
```
pip install -r requirements.txt
```

Run:
```
python3 manage.py runserver
```
In your browser, search...<br><br>
127.0.0.1:8000/lstmData/{requested stock ticker}?format=json

![Screenshot 2024-02-03 172129](https://github.com/Fadeleke57/bonsai-finance-app/assets/110058327/7a914a7a-71ad-4cb4-b2d4-55bd6657e203)
![Screenshot 2024-02-03 171820](https://github.com/Fadeleke57/bonsai-finance-app/assets/110058327/6c2876a0-c8d7-440d-b284-169d643c69ef)


