from django.urls import path
from .views import PhotosAPIView
#chezdior: best food in dc

urlpatterns = [
    path('', PhotosAPIView.as_view(), name='photos_home'),
]
