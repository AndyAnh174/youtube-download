from ninja import Router, Schema
from django.conf import settings
import yt_dlp
import os
import uuid
from django.http import JsonResponse

router = Router()

class DownloadRequest(Schema):
    url: str

@router.post("/process")
def process_video(request, payload: DownloadRequest):
    video_url = payload.url
    
    # Validation cơ bản
    if "youtube.com" not in video_url and "youtu.be" not in video_url:
        return JsonResponse({"error": "Invalid URL. Please provide a Youtube link."}, status=400)

    # Thư mục lưu file
    download_path = os.path.join(settings.MEDIA_ROOT, 'downloads')
    os.makedirs(download_path, exist_ok=True)
    
    # Tạo tên file unique để tránh trùng lặp tạm thời
    # Chúng ta sẽ dùng title của video làm tên file cuối cùng, nhưng để yt-dlp xử lý
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True,
        'noplaylist': True, # Chỉ tải video đơn, không tải cả playlist
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            
            # Lấy thông tin file đã tải
            filename = ydl.prepare_filename(info)
            # Sau khi post-process, extension đổi thành mp3
            base_filename = os.path.splitext(os.path.basename(filename))[0]
            final_filename = f"{base_filename}.mp3"
            
            # Trả về đường dẫn download
            file_url = f"{settings.MEDIA_URL}downloads/{final_filename}"
            
            return {
                "success": True,
                "title": info.get('title', 'Unknown Title'),
                "download_url": file_url,
                "thumbnail": info.get('thumbnail', ''),
                "duration": info.get('duration_string', '')
            }

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
