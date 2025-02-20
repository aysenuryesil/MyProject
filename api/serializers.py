from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task

class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1, required=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserAddSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, required=True)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TaskAddSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=True)
    description = serializers.CharField(max_length=1000, required=False)