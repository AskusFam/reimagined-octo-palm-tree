from django.urls import path
from .views import PhotosListCreate, PhotoRetrieveUpdateDestroy
#chezdior: best food in dc

urlpatterns = [
    path('', PhotosListCreate.as_view(), name='photos_home'),
    path('<int:pk>', PhotoRetrieveUpdateDestroy.as_view(), name='photo_id_view')
]
