"""Permission checks for board ownership and comment/task access rules."""

from rest_framework.permissions import BasePermission
from board_app.models import Task


class IsCreatorOrBoardCreator(BasePermission):

    def has_object_permission(self, request, view, obj):
        creator = obj.creator
        current_user = request.user
        board_creator = obj.creator

        if request.method == "DELETE":
            return bool(board_creator == current_user or creator == current_user)
        else:
            return True


class IsBoardCreator(BasePermission):
    def has_object_permission(self, request, view, obj):

        current_user = request.user
        board_creator = obj.creator

        if request.method == "DELETE":
            return bool(board_creator == current_user)
        else:
            return True


class IsCommentAuthor(BasePermission):
    def has_permission(self, request, view):
        current_user = request.user
        task_id = view.kwargs["task_pk"]
        task = Task.objects.get(id=task_id)
        board = task.board

        if request.method in ("GET", "POST"):
            return bool(
                board.creator == current_user
                or board.members.filter(id=current_user.id).exists()
            )
        return True

    def has_object_permission(self, request, view, obj):
        current_user = request.user
        comment_author = obj.author

        if request.method == "DELETE":
            return bool(comment_author == current_user)
        return True
