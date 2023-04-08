from django.urls import path
from .views import PhotosAPIView, PhotoRetrieveUpdateDestroy
#chezdior: best food in dc

urlpatterns = [
    path('', PhotosAPIView.as_view(), name='photos_home'),
    path('<int:pk>', PhotoRetrieveUpdateDestroy.as_view(), name='photo_id_view')
]
