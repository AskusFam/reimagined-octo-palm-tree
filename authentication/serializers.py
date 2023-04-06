from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=False)
    is_staff = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2','is_staff', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        
        if 'password2' in attrs:
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"password": "Password fields didn't match."})
        elif attrs['is_staff']:
            raise serializers.ValidationError({"password2": "Password2 field must be set to use is_staff feild."})

        

        return attrs

    def create(self, validated_data):
        if 'password2' in validated_data:
            del validated_data['password2']
        user = User.objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.is_staff = validated_data['is_staff']
        user.save()

        return user