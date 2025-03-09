import io
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
            'outtmpl': 'media/%(title)s.%(ext)s',
            'merge_output_format': 'mp4', 
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
        }

        # Get the video
        with YoutubeDL(OPTIONS) as ydl:
            stream = ydl.extract_info(url, download=True)

        video_filename = f"media/{stream['title']}.mp4"

        def file_iterator(filename, chunk_size=8192):
            with open(filename, "rb") as f:
                while chunk := f.read(chunk_size):
                    yield chunk


        # Return response
        response_video = StreamingHttpResponse(file_iterator(video_filename), content_type='video/mp4')
        response_video['Content-Disposition'] = f'attachment'
        return response_video

    except Exception as e:
        import traceback
        print("🔥 ERROR EN DESCARGA 🔥")
        traceback.print_exc()
        return Response({'Unexpected error': str(e)}, status=500)