from rest_framework import serializers
from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='creator.username')
    image = serializers.ImageField(write_only=True)

    class Meta:
        model = Photo
        fields = ('id', 'title', 'path_to_store', 'year', 'image', 'creator', 'created_at', 'updated_at')
        read_only_fields = ['id', 'created_at', 'path_to_store']
    
    def create(self, validated_data):
        if 'path_to_store' in validated_data and 'image' not in validated_data:
            return Photo.objects.create(**validated_data)