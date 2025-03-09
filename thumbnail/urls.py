from django.urls import path
from .views import test_view
from .views import get_thumbnail

urlpatterns = [
    path('thumbnail/', get_thumbnail),
    path('/', test_view),
]