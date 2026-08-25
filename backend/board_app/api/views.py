from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import BoardSerializer, TaskSerializer, TaskCommentSerializer
from board_app.models import Task, Board, TaskComment
from django.contrib.auth.models import User
from django.db.models import Q



class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(
            Q(creator=user) | Q(members=user)
        )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)




class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    
class TaskCommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer