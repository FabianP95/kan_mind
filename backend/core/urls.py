"""Root URL configuration for the KanMind Django project."""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user_auth_app.api.urls')),
    path('api/', include('board_app.api.urls')),
]
