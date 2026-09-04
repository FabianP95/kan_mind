"""API viewsets for managing boards, tasks, and task comments."""

from django.db.models import Q
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    BoardSerializer,
    TaskSerializer,
    TaskCommentSerializer,
    BoardDetailSerializer,
    UpdateBoardSerializer,
)
from board_app.models import Task, Board, TaskComment
from .permissions import IsCreatorOrBoardCreator, IsBoardCreatorOrMember, IsCommentAuthor


class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsBoardCreatorOrMember]
    serializer_class = BoardSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BoardDetailSerializer
        if self.action == "update" or self.action == "partial_update":
            return UpdateBoardSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.action == "list":
            user = self.request.user
            return Board.objects.filter(Q(creator=user) | Q(members=user)).distinct()
        else:
            return Board.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsCreatorOrBoardCreator]
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        if self.action == "list":
            user = self.request.user
            return Task.objects.filter(Q(board__creator=user) | Q(board__members=user)).distinct()
        else:
            return Task.objects.all()

    @action(detail=False, methods=["get"], url_path="assigned-to-me")
    def assigned_to_me(self, request):
        user = self.request.user
        tasks = Task.objects.filter(assignee=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="reviewing")
    def reviewing(self, request):
        user = self.request.user
        tasks = Task.objects.filter(reviewer=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskCommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsCommentAuthor]
    serializer_class = TaskCommentSerializer

    def get_queryset(self):
        task_id = self.kwargs["task_pk"]
        return TaskComment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        task_id = self.kwargs["task_pk"]
        serializer.save(author=self.request.user, task_id=task_id)
