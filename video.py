import os
import yt_dlp

def download_youtube_content(urls, output_path, format='mp4'):
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': 'best',  # This will get the best quality single file
    }

    if format == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    elif format == 'mp4':
        ydl_opts.update({
            'format': 'best[ext=mp4][height<=480][fps<=30]/best[ext=mp4]/best',
        })

    for url in urls:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info['duration'] > 900:  # 900 seconds = 15 minutes
                    print(f"Skipping video at {url} because it is longer than 15 minutes.")
                    continue
                
                print(f"Downloading {'audio' if format == 'mp3' else 'video'} from {url}...")
                ydl.download([url])
            print("Download completed!")

        except Exception as e:
            print(f"An error occurred with video at {url}: {str(e)}")

# Example usage
urls = input("Enter the YouTube video URLs (comma separated): ").split(',')
urls = [url.strip() for url in urls]
format = input("Enter the desired format (mp4/mp3): ").lower()
output_path = input("Enter the output directory path: ")

download_youtube_content(urls, output_path, format)