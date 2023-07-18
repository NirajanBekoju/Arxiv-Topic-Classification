from django.urls import path 
from .views import ModelPrediction 

urlpatterns = [
    path('predict/', ModelPrediction.as_view()),
]