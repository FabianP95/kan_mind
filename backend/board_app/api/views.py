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
        return Board.objects.filter(Q(creator=user) | Q(members=user))

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewer=user , board=self.request.board.id)
    
    def get_queryset(self):
            user = self.request.user
            return Task.objects.filter(assignee=user , board=self.request.board.id)


class TaskCommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskCommentSerializer

    def get_queryset(self):
        user = self.request.user
        return TaskComment.objects.filter(Q(creator=user) | Q(members=user))
