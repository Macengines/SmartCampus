import yt_dlp

video_url = input("Enter the YouTube video URL: ")

ydl_opts = {
    'format': 'best',  # best quality
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])
