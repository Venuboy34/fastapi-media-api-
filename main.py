from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Define a model for the incoming request
class DownloadRequest(BaseModel):
    platform: str
    media_type: str
    media_id: str  # ID of the media to download, could be a URL or specific ID depending on the platform

@app.get("/api/download")
async def download_media(request: DownloadRequest):
    platform = request.platform.lower()
    media_type = request.media_type.lower()
    media_id = request.media_id

    # Define the download logic for each platform
    if platform == "instagram":
        if media_type == "reels":
            # Example: Download logic for Instagram reels
            url = f"https://api.instagram.com/reels/{media_id}"  # Use proper Instagram API or scraping method
        elif media_type == "posts":
            url = f"https://api.instagram.com/posts/{media_id}"
        elif media_type == "stories":
            url = f"https://api.instagram.com/stories/{media_id}"
        else:
            raise HTTPException(status_code=400, detail="Invalid media type for Instagram")

    elif platform == "pinterest":
        if media_type == "videos":
            url = f"https://api.pinterest.com/videos/{media_id}"
        elif media_type == "stories":
            url = f"https://api.pinterest.com/stories/{media_id}"
        else:
            raise HTTPException(status_code=400, detail="Invalid media type for Pinterest")

    elif platform == "tiktok":
        if media_type == "videos":
            url = f"https://api.tiktok.com/videos/{media_id}"
        elif media_type == "photos":
            url = f"https://api.tiktok.com/photos/{media_id}"
        elif media_type == "audio":
            url = f"https://api.tiktok.com/audio/{media_id}"
        else:
            raise HTTPException(status_code=400, detail="Invalid media type for TikTok")

    # Repeat similar logic for other platforms (Twitter, VK, Reddit, etc.)

    else:
        raise HTTPException(status_code=400, detail="Invalid platform")

    # Assuming a generic download method
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Save the file (you can modify how you save the file depending on your requirements)
            filename = f"{platform}_{media_type}_{media_id}.mp4"
            with open(filename, "wb") as file:
                file.write(response.content)
            return {"status": "success", "message": f"Downloaded {filename}"}
        else:
            raise HTTPException(status_code=500, detail="Failed to download media")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
