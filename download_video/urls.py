from django.urls import path
from .views import download_video
from .views import get_info_video

urlpatterns = [
    path('download/', download_video),
    path('getinfo/', get_info_video)
]