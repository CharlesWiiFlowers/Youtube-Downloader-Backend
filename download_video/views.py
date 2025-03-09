import io
from django.http import FileResponse, StreamingHttpResponse
from pytube import YouTube
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
        
        # Get the video
        yt = YouTube(str(url))
        stream = yt.streams.get_highest_resolution()

        # Make the buffer
        buffer = io.BytesIO()
        stream.stream_to_buffer(buffer)
        buffer.seek(0)

        # Return response
        response_video = StreamingHttpResponse(buffer, content_type='video/mp4')
        response_video['Content-Disposition'] = f'attachment; filename="{stream.default_filename}.mp4"'
        return response_video

    except Exception as e:
        import traceback
        print("🔥 ERROR EN DESCARGA 🔥")
        traceback.print_exc()
        return Response({'Unexpected error': str(e)}, status=500)