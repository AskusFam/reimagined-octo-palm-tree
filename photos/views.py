from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Photo
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import PhotoSerializer
from .permissions import isCreatorOrSafeMethod
from rest_framework.response import Response
from .utils import create_photo, delete_photo


class PhotosListCreate(ListCreateAPIView):
    queryset = Photo.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer = create_photo(serializer)
            serializer.save(creator=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        delete_photo(serializer.validated_data['path_to_store'])
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated, isCreatorOrSafeMethod]
    queryset = Photo.objects.all()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        Photos = self.get_object()
        path = Photos.path_to_store
        delete_photo(path)
        return self.destroy(request, *args, **kwargs)
