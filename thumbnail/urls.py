from django.urls import path
from .views import get_thumbnail

urlpatterns = [
    path('thumbnail/', get_thumbnail)
]