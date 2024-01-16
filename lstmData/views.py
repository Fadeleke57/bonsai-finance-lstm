from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .lstmModelDriver.driver import Driver
from .lstmModelDriver.config import Configurations

from datetime import datetime
 
class StockPrediction:
    def __init__(self, stock_symbol, predicted_price):
        self.stock_symbol = stock_symbol
        self.predicted_price = predicted_price
        self.prediction_date = datetime.now()

    def to_json(self):
        return {
            "stockSymbol": self.stock_symbol,
            "predictedPrice": self.predicted_price,
            "predictionDate": self.prediction_date.strftime('%m/%d/%Y %H:%M:%S')
        }
      
@api_view(['GET'])      
def lstmData_detail(request, ticker, format=None):
    try:
        configs = Configurations.get_configs(ticker)
        predictedPrice = Driver.get_price(configs)

        # prediction variable for instance of StockPrediction
        prediction = StockPrediction(ticker, predictedPrice)

        # JSON response
        response_data = {
            "status": "success",
            "data": prediction.to_json(),
            "message": f"Next day stock price prediction for {ticker.upper()}"
        }

        return Response({"Response": response_data})

    except Exception as e:
        error_response = {
            "status": "error",
            "message": str(e) or "An error occurred while processing the request."
        }
        return Response({"Response": error_response}, status=status.HTTP_400_BAD_REQUEST)

