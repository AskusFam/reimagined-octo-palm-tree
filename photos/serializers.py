from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Photo
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class PhoteSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='creator.username')
    
    class Meta:
        model = Photo
        fields = ('id', 'title', 'path_to_store', 'year', 'creator', 'created_at', 'updated_at')
    
