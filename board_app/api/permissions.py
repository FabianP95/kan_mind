"""Permission checks for board ownership and comment/task access rules."""

from rest_framework.permissions import BasePermission
from rest_framework.generics import get_object_or_404
from board_app.models import Task, Board


class IsCreatorOrBoardCreator(BasePermission):

    def has_permission(self, request, view):

        if request.method == "POST":
            board_id = request.data.get("board")
            if not board_id:
                return False
            board = get_object_or_404(Board, id=board_id)
            user = request.user
            return bool(
                board.creator == user or board.members.filter(id=user.id).exists()
            )
        return True

    def has_object_permission(self, request, view, obj):

        if request.method in ("PATCH", "PUT"):
            user = request.user
            return bool(
                obj.board.creator == user
                or obj.board.members.filter(id=user.id).exists()
            )

        if request.method == "DELETE":
            user = request.user
            return bool(obj.creator == user or obj.board.creator == user)
        return True


class IsBoardCreatorOrMember(BasePermission):

    def has_permission(self, request, view):
        
        
        if request.method == "GET" and view.action == "retrieve":
            current_user = request.user
                    
            board_id = view.kwargs["pk"]
            board = get_object_or_404(Board, id = board_id)
            board_creator = board.creator
            
            return bool(board_creator == current_user or board.members.filter(id=current_user.id).exists())
        else: 
            return True

    def has_object_permission(self, request, view, obj):

        current_user = request.user
        board_creator = obj.creator
        members = obj.members

        if request.method in ("PATCH", "PUT"):
            return bool(board_creator == current_user or members.filter(id=current_user.id).exists())
        elif request.method == "DELETE":
            return bool(board_creator == current_user)
        else: 
            return bool(board_creator == current_user or members.filter(id=current_user.id).exists())
       


class IsCommentAuthor(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "POST"):
            task_id = view.kwargs["task_pk"]
            task = get_object_or_404(Task, id=task_id)
            board = task.board
            current_user = request.user

            return bool(
                board.creator == current_user
                or board.members.filter(id=current_user.id).exists()
            )
        return True

    def has_object_permission(self, request, view, obj):

        if request.method == "DELETE":
            return bool(obj.author == request.user)
        return True
