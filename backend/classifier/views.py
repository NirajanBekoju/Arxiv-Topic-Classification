from rest_framework.views import APIView 
from rest_framework.response import Response 
from .process import predict 
import numpy as np 


class ModelPrediction(APIView):
    def post(self, request, format = None):
        data = request.data 
        text = data["text"]
        result = predict(text)
        return Response(result)