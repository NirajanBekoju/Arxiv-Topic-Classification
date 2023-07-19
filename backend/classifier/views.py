from rest_framework.views import APIView 
from rest_framework.response import Response 
from .process import predict 
import numpy as np 


class ModelPrediction(APIView):
    def post(self, request, format = None):
        data = request.data 
        text = data["abstract"]
        tag_no = 3
        if "tag_no" in data:
            tag_no = int(data["tag_no"])
        if text == "":
            return Response({"error" : "No abstract"})
        result = predict(text, top_k = tag_no)
        return Response(result)
