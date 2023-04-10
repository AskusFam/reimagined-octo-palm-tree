from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Photo
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import PhotoSerializer
from .permissions import isCreatorOrSafeMethod
from rest_framework.response import Response
from azure.storage.blob import BlobServiceClient
import uuid
import os
# Create your views here.
from environs import Env

env = Env()
env.read_env()

class PhotosAPIView(ListCreateAPIView):
    queryset = Photo.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        '''
        We will still call the super post function.
        First we will make sure we send the image to the blob storage
        Then call the create funtion
        '''
        serializer = PhotoSerializer(data=request.data)
        #print (request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data  # get unsaved instance of the model
            image = valid_data['image']
            serializer.validated_data['creator'] = request.user
            del serializer.validated_data['image']
            
            image_name = str(uuid.uuid4())
            
            blob_service_client = BlobServiceClient.from_connection_string(env.str('CONNECTION_STRING'))
            container_client = blob_service_client.get_container_client(env.str('CONTAINER_NAME'))
            blob_client = container_client.get_blob_client(image_name)
            blob_client.upload_blob(image)
            serializer.validated_data['path_to_store'] = blob_client.url
                
            serializer.save()
            #serializer = PhotoSerializer(photo)  # reserialize the saved instance
            

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class PhotoRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated, isCreatorOrSafeMethod]
    queryset = Photo.objects.all()
    
    def delete(self, request, *args, **kwargs):
        Photos = self.get_object()
        path = Photos.path_to_store
        directory = os.path.dirname(path) 
        filename = os.path.basename(path)

        # Get the BlobClient for the file you want to delete
        blob_service_client = BlobServiceClient.from_connection_string(env.str('CONNECTION_STRING'))
        container_client = blob_service_client.get_container_client(env.str('CONTAINER_NAME'))
        blob_client = container_client.get_blob_client(filename)

       
        blob_client.delete_blob()
        return self.destroy(request, *args, **kwargs)