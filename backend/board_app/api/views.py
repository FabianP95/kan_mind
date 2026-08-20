from rest_framework import status
from rest_framework import viewsets
from .serializers import BoardSerializer, TaskSerializer
from board_app.models import Task, Board



class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer




class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer