from rest_framework import serializers
from board_app.models import Board, Task


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task

    
