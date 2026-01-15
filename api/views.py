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
    
    if "youtube.com" not in video_url and "youtu.be" not in video_url:
        return JsonResponse({"error": "Invalid URL. Please provide a Youtube link."}, status=400)

    download_path = os.path.join(settings.MEDIA_ROOT, 'downloads')
    os.makedirs(download_path, exist_ok=True)
    
    # Use a random ID for the temporary filename to avoid shell/encoding issues
    temp_id = str(uuid.uuid4())
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'outtmpl': os.path.join(download_path, f'{temp_id}.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }

    try:
        from django.utils.text import slugify
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get info directly inside the download context
            info = ydl.extract_info(video_url, download=True)
            
            original_title = info.get('title', 'audio')
            
            # "Ghi cai title ko dau" -> Convert to ASCII slug
            clean_title = slugify(original_title)
            if not clean_title:
                clean_title = f"audio-{temp_id[:8]}"
                
            # Final filename: clean_title.mp3
            # Check if file exists, if so append random
            final_filename = f"{clean_title}.mp3"
            final_path = os.path.join(download_path, final_filename)
            
            if os.path.exists(final_path):
                 final_filename = f"{clean_title}-{temp_id[:4]}.mp3"
                 final_path = os.path.join(download_path, final_filename)
            
            # The file currently looks like temp_id.mp3
            temp_file_path = os.path.join(download_path, f"{temp_id}.mp3")
            
            # Rename if exists
            if os.path.exists(temp_file_path):
                os.rename(temp_file_path, final_path)
            
            file_url = f"{settings.MEDIA_URL}downloads/{final_filename}"
            
            return {
                "success": True,
                "title": original_title, # Show original title in UI
                "download_url": file_url,
                "thumbnail": info.get('thumbnail', ''),
                "duration": info.get('duration_string', '')
            }

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
