from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Photo
from rest_framework.permissions import IsAuthenticated
from .serializers import PhoteSerializer
# Create your views here.

class PhotosAPIView(ListCreateAPIView):
    queryset = Photo.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PhoteSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
