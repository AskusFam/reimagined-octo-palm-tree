from azure.storage.blob import BlobServiceClient
import uuid
from environs import Env
import uuid
import os
env = Env()
env.read_env()


def create_photo(serializer):
    '''
    This function will create/upload a photo to the azure blob storage
    It creates a uuid for the for the name of the image which avoids issues related
    to having the same name. 
    Args:
        serializer (serializer): This is a serializer object and holds 
        all of the data recieved from our API.

    Returns:
        Serializer: Returns the serialzier objec with the validated data altered.
    '''
    valid_data = serializer.validated_data  # get unsaved instance of the model
    image = valid_data['image']
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
    '''
    This function will delete/destory a photo to the azure blob storage
    It takes the path of from the object and pulls the name from it. That name 
    is used to delete the file in the blob.
    Args:
        Path (string): This is a serializer object and holds 
        all of the data recieved from our API.

    Returns:
        None: Nothing returned from this function.
    '''
    directory = os.path.dirname(path)
    filename = os.path.basename(path)

    blob_service_client = BlobServiceClient.from_connection_string(
        env.str('CONNECTION_STRING'))
    container_client = blob_service_client.get_container_client(
        env.str('CONTAINER_NAME'))
    blob_client = container_client.get_blob_client(filename)

    blob_client.delete_blob()
