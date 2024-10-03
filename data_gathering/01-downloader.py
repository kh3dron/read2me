import yt_dlp
import os

def download_youtube_audio(url, output_dir='../data/audio'):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }

    # Download the audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    
    video_url = "https://www.youtube.com/watch?v=zNjhzdvAEUI"
    download_youtube_audio(video_url)
    print("Download complete. The MP3 file has been saved to the 'data' directory.")
