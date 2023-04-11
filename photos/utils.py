from azure.storage.blob import BlobServiceClient
import uuid
from environs import Env
import uuid
import os
env = Env()
env.read_env()


def create_photo(serializer):
    valid_data = serializer.validated_data  # get unsaved instance of the model
    image = valid_data['image']
    del serializer.validated_data['image']
    image_name = str(uuid.uuid4())

    blob_service_client = BlobServiceClient.from_connection_string(
        env.str('CONNECTION_STRING'))
    container_client = blob_service_client.get_container_client(
        env.str('CONTAINER_NAME'))
    blob_client = container_client.get_blob_client(image_name)
    blob_client.upload_blob(image)
    serializer.validated_data['path_to_store'] = blob_client.url

    return serializer


def delete_photo(path):
    directory = os.path.dirname(path)
    filename = os.path.basename(path)

    blob_service_client = BlobServiceClient.from_connection_string(
        env.str('CONNECTION_STRING'))
    container_client = blob_service_client.get_container_client(
        env.str('CONTAINER_NAME'))
    blob_client = container_client.get_blob_client(filename)

    blob_client.delete_blob()
