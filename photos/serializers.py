from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Photo
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class PhotoSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='creator.username')
    image = serializers.ImageField(write_only=True)

    class Meta:
        model = Photo
        fields = ('id', 'title', 'path_to_store', 'year', 'image', 'creator', 'created_at', 'updated_at')
        read_only_fields = ['id', 'created_at', 'path_to_store']
    
    def create(self, validated_data):
        if 'path_to_store' in validated_data:
            print ('good')
        return Photo.objects.create(**validated_data)
       