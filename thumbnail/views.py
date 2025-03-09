from pytube import YouTube

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def test_view(request):
    return Response({'Message': 'Hello CatWorld! 🐈‍⬛'})

# TO DO: Implement get_thumbnail
@api_view(['GET'])
def get_thumbnail(request):
    """Return a video info"""

    url = request.GET.get('url')
    if not url:
        return Response({'error': 'Missing URL parameter'}, status=400)
    
    return Response(url)