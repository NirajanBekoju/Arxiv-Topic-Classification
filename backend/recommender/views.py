from rest_framework.views import APIView 
from rest_framework.response import Response 
import numpy as np 
from .process import getRecommendation
import json


class Recommendation(APIView):
    def post(self, request, format = None):
        data = request.data 
        text = data["description"]
        top_k = 3
        if "top_k" in data:
            top_k = int(data["top_k"])
        result = getRecommendation(text, top_k=top_k)
        return Response(result)
