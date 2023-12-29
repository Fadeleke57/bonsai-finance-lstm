from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse

#from .models import lstmData
#from .serializers import lstmDataSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .lstmModelDriver.driver import Driver
from .lstmModelDriver.config import Configurations

from datetime import datetime

'''
@api_view(['GET', 'POST'])
def lstmData_list(request, format = None):

    if request.method == 'GET':
        data_points = lstmData.objects.all()
        serializer = lstmDataSerializer(data_points, many=True)
        return Response({
            "status": "success",
            "data": serializer.data,
            "message": "List of stock predictions"
        })
    
    if request.method == 'POST':
        serializer = lstmDataSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                    "status": "success",
                    "data": serializer.data,
                    "message": "New stock prediction created"
            }, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''  
class StockPrediction:
    def __init__(self, stock_symbol, predicted_price):
        self.stock_symbol = stock_symbol
        self.predicted_price = predicted_price
        self.prediction_date = datetime.now().date()

    def to_json(self):
        return {
            "stockSymbol": self.stock_symbol,
            "predictedPrice": self.predicted_price,
            "predictionDate": self.prediction_date.strftime('%Y-%m-%d')
        }
      
@api_view(['GET'])      
def lstmData_detail(request, ticker, format=None):
    try:
        configs = Configurations.get_configs(ticker)
        predictedPrice = Driver.get_price(configs)

        if predictedPrice is None:
            raise ValueError("Failed to predict price for the given ticker.")

        # Create an instance of StockPrediction
        prediction = StockPrediction(ticker, predictedPrice)

        # Prepare the JSON response
        return Response({
            "Response": {
                "status": "success",
                "data": prediction.to_json(),
                "message": f"Next day stock price prediction for {ticker.upper()}"
            }
        })

    except Exception as e:
        return Response({
            "Response": {
                "status": "error",
                "message": str(e) or "An error occurred while processing the request."
            }  
        }, status=status.HTTP_400_BAD_REQUEST)

"""  
elif request.method == 'PUT':
    serializer = lstmDataSerializer(ldata, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "data": serializer.data,
            "message": f"Stock prediction for {ldata.stockSymbol} updated"
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

elif request.method == 'DELETE':
    lstmData.delete()
    return Response({
        "status": "success",
        "message": "Stock prediction deleted"
    }, status=status.HTTP_204_NO_CONTENT)
"""      
