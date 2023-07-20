from django.urls import path 
from .views import Recommendation 

urlpatterns = [
    path('recommend/', Recommendation.as_view()),
]