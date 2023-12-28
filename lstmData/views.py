from django.shortcuts import render
from django.http import JsonResponse
from .models import lstmData
from .serializers import lstmDataSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .lstmModelDriver.driver import Driver


@api_view(['GET', 'POST'])
def lstmData_list(request, format = None):

    if request.method == 'GET':
        data_points = lstmData.objects.all()
        serializer = lstmDataSerializer(data_points, many=True)
        return JsonResponse({"response_data": serializer.data})
    
    if request.method == 'POST':
        serializer = lstmDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'PUT','DELETE'])      
def lstmData_detail(request, id, format=None):
    try:
        ldata = lstmData.objects.get(pk=id)
    except lstmData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = lstmDataSerializer(ldata)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = lstmDataSerializer(ldata, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        lstmData.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
