import yt_dlp
import os

TITLE = "mike"
VIDEO_URL = "https://www.youtube.com/watch?v=zNjhzdvAEUI"

def download_youtube_audio(url, output_dir=f'../data/audio/{TITLE}'):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, f"full.%(ext)s"),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    download_youtube_audio(VIDEO_URL)
    print("Download complete. The WAV file has been saved to the 'data' directory.")