
from django.urls import path, include
from rest_framework import routers

from .views import BoardViewSet, TaskViewSet, TaskCommentViewSet

router =routers.SimpleRouter()
router.register(r'boards', BoardViewSet, basename='board')
router.register(r'tasks', TaskViewSet)
router.register(r'taskcomments', TaskCommentViewSet)



urlpatterns = [
    path("", include(router.urls)),
]