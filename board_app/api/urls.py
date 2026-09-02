"""URL routing for board-related API endpoints and nested task comments."""

from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter

from .views import BoardViewSet, TaskViewSet, TaskCommentViewSet

router = routers.SimpleRouter()
router.register(r'boards', BoardViewSet, basename='board')
router.register(r'tasks', TaskViewSet, basename='task')

tasks_router = NestedDefaultRouter(router, r'tasks', lookup='task')
tasks_router.register(r'comments', TaskCommentViewSet, basename='task-comments')

urlpatterns = [
    path("", include(router.urls)),
    path("", include(tasks_router.urls)),
]
