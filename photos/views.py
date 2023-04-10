from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Photo
from rest_framework.permissions import IsAuthenticated
from .serializers import PhoteSerializer
from .permissions import isCreatorOrSafeMethod
# Create your views here.

class PhotosAPIView(ListCreateAPIView):
    queryset = Photo.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PhoteSerializer

    def post(self, request, *args, **kwargs):
        '''
        We will still call the super post function.
        First we will make sure we send the image to the blob storage
        Then call the create funtion
        '''
        return super().post(request, *args, **kwargs)
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class PhotoRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = PhoteSerializer
    permission_classes = [IsAuthenticated, isCreatorOrSafeMethod]
    queryset = Photo.objects.all()
    
