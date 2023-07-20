from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/classfier/', include('classifier.urls')),
    path('api/recommender/', include('recommender.urls'))
]
