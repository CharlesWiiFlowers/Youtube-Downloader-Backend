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
            'outtmpl': 'media/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'cookies-from-browser': 'firefox', 
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

    clean_code()

    URL = request.GET.get('url')
    if not URL:
        return Response({'error': 'Missing URL parameter'}, status=400)

    OPTIONS = {
        'format': 'bestvideo+bestaudio/best',
        'restrictfilenames': True,
        'outtmpl': 'media/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }

    try:
        # Get the video
        with YoutubeDL(OPTIONS) as ydl:
            stream = ydl.extract_info(URL, download=True)

        video_filename = stream['requested_downloads'][0]['filepath']
        response_video = StreamingHttpResponse(file_iterator(video_filename), content_type='video/mp4')
        response_video['Content-Disposition'] = f'attachment; filename="{stream["title"]}.mp4"'

        return response_video

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'Unexpected error': str(e)}, status=500)

def file_iterator(filename, chunk_size=8192):
        with open(filename, "rb") as f:
            while chunk := f.read(chunk_size):
                yield chunk

def clean_code():
    """This function is used to clean the code"""

    # Delete the media files
    import os
    for file in os.listdir('media/'):
        os.remove(f'media/{file}')

    print("Code cleaned")