# REST API For Next Day Prices
Bi-layer LSTM model, enabling next-day price forecasting and providing outputs in JSON format upon request. *Useability is restricted at the moment due to the size of pytorch's packages but a demonstration is provided below*. 

### Prerequisites:
Python3<br>
Django<br>

### Installation:
First, clone this repository to your local machine:
```
git clone https://github.com/Fadeleke57/bonsai-finance-app.git
cd bonsai-finance-app
```

Install Django Rest Framework and Django Depug Toolbar:
```
pip install -r requirements.txt
```

Run:
```
python3 manage.py runserver
```
In your browser, search...<br><br>
127.0.0.1:8000/lstmData/{requested stock ticker}

![Screenshot 2024-02-03 172129](https://github.com/Fadeleke57/bonsai-finance-app/assets/110058327/7a914a7a-71ad-4cb4-b2d4-55bd6657e203)
![Screenshot 2024-02-03 171820](https://github.com/Fadeleke57/bonsai-finance-app/assets/110058327/6c2876a0-c8d7-440d-b284-169d643c69ef)


