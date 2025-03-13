import io
import ffmpeg
from django.http import FileResponse, JsonResponse, StreamingHttpResponse
from yt_dlp import YoutubeDL
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def get_info_video(request):
    """Get the information of the video on the given URL"""

    URL = request.GET.get('url')
    if not URL:
        return Response({'error': 'Missing URL parameter'}, status=400)

    FORMAT = request.GET.get('format')
    if not FORMAT:
        # return Response({'error': 'Missing URL parameter'}, status=400) TODO: UNCOMMENT THIS LINE
        FORMAT = 'bestvideo+bestaudio/best' # TODO: REMOVE THIS LINE

    try:
        
        OPTIONS = {
            'format': FORMAT,
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4', 
        }

        # Get the video
        with YoutubeDL(OPTIONS) as ydl:
            video_info = ydl.extract_info(URL, download=True)
            print(video_info)

        return JsonResponse(video_info, status=200)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'Unexpected error': str(e)}, status=500)

    
@api_view(['GET'])
def download_video(request):
    """Download the video on the given URL"""