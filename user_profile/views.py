from unittest import result

from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
import yt_dlp
from django.contrib.auth.decorators import login_required

from users.models import Account


# Create your views here.
#@login_required(login_url='login')
def search(request):
    if request.method!='GET': return JsonResponse({'message': 'Wrong request method!'}, status=400)

    user_id=request.session.get('user_id')
    user=Account.objects.filter(id=user_id).first()


    if user is None:
        return render(request, 'login.html')

    query=request.GET.get('q', '').strip()

    if query=='': return JsonResponse({'message': "Write anything!"}, status=400)

    results=[]
    print(f'this is query: {query}')
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch10:{query}", download=False)
        if info and "entries" in info:
            for entry in info["entries"]:
                video_id = entry.get("id")
                results.append(
                    {
                        "id": video_id,
                        "title": entry.get("title", "Unknown Title"),
                        "uploader": entry.get("uploader", "YouTube Channel"),
                        "thumbnail": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
                    }
                )


    return render(request, 'profile.html', {'query': query, 'results': results})


#@login_required(login_url='login')
def get_stream(request):
    user_id = request.session.get('user_id')
    user = Account.objects.filter(id=user_id).first()

    if user is None:
        #return render(request, 'login.html')
        return JsonResponse({'message': "Required login!"}, status=400)

    video_id = request.GET.get("id")

    print(f'it reach here and video id is {video_id}')
    if not video_id:
        return JsonResponse({"error": "No video ID provided"}, status=400)

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    # Extract direct MP4 stream URL (combines video + audio)
    '''ydl_opts = {
        "format": "best[ext=mp4]/best",
        "quiet": True,
    }'''

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "quiet": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["web", "android", "mweb"]
            }
        },
        "socket_timeout": 30,
        "geo_bypass": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            # Direct stream link from GoogleVideo servers
            stream_url = info.get("url")

            if stream_url:
                return JsonResponse({"stream_url": stream_url})
            return JsonResponse({"error": "Could not extract stream URL"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)