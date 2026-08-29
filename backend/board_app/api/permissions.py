from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


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