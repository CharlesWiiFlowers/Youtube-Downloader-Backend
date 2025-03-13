import io
import ffmpeg
from django.http import FileResponse, StreamingHttpResponse
from yt_dlp import YoutubeDL
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def download_video(request):
    """Download the video on the given URL"""

    url = request.GET.get('url')
    if not url:
        return Response({'error': 'Missing URL parameter'}, status=400)

    try:
        
        OPTIONS = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4', 
        }

        buffer = io.BytesIO()

        # Get the video
        with YoutubeDL(OPTIONS) as ydl:
            buffer.write(ydl.extract_info(url, download=True))

        buffer.seek(0)
        print(buffer)

        # Return response
        response_video = StreamingHttpResponse(buffer, content_type='video/mp4')
        response_video['Content-Disposition'] = f'attachment'
        return response_video

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'Unexpected error': str(e)}, status=500)