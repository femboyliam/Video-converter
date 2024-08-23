import os
import yt_dlp
import sys
import logging

logging.basicConfig(filename='downloader.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def download_content(urls, output_path, content_type='youtube', format='mp4'):
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'progress_hooks': [logging_hook],
    }

    # Configure ydl options based on content type
    if content_type == 'youtube':
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
                'format': 'best[ext=mp4]/best',
            })

    elif content_type == 'twitter':
        ydl_opts.update({
            'format': 'best[ext=mp4]/best',
        })
        
    elif content_type == 'spotify':
        if format == 'mp3':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            logging.error("Invalid format for Spotify. Only MP3 is allowed.")
            print("Invalid format for Spotify. Only MP3 is allowed.")
            return

    for url in urls:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logging.info(f"Starting download for {url}")
                info = ydl.extract_info(url, download=False)
                if content_type == 'youtube' and info['duration'] > 1000:
                    logging.warning(f"Skipping video at {url} because it is longer than 15 minutes.")
                    print(f"Skipping video at {url} because it is longer than 15 minutes.")
                    continue
                
                print(f"Downloading {'audio' if format == 'mp3' else 'video'} from {url}...")
                ydl.download([url])
            logging.info(f"Download completed for {url}")
            print("Download completed!")

        except yt_dlp.utils.DownloadError as e:
            logging.error(f"Download error for {url}: {str(e)}")
            print(f"Download error for {url}: {str(e)}")
        except Exception as e:
            logging.error(f"An unexpected error occurred with content at {url}: {str(e)}")
            print(f"An unexpected error occurred with content at {url}: {str(e)}")

def logging_hook(d):
    if d['status'] == 'finished':
        logging.info('Done downloading, now converting ...')
    elif d['status'] == 'downloading':
        percent = d['_percent_str']
        speed = d['_speed_str']
        eta = d['_eta_str']
        logging.debug(f'Downloading: {percent} at {speed} ETA: {eta}')

try:
    urls = input("Enter the video or music URLs (comma separated): ").split(',')
    urls = [url.strip() for url in urls]

    content_type = input("Enter the desired content type (youtube/twitter/spotify): ").lower()
    if content_type not in ['youtube', 'twitter', 'spotify']:
        raise ValueError("Invalid content type. Please enter youtube, twitter, or spotify.")

    if content_type == 'twitter':
        format = 'mp4'
    elif content_type == 'spotify':
        format = 'mp3'
    else:
        format = input("Enter the desired format (mp4/mp3): ").lower()

    output_path = input("Enter the output directory path: ")
    if not os.path.exists(output_path):
        raise ValueError("Invalid path. Please provide a valid output directory.")

    download_content(urls, output_path, content_type, format)

except Exception as e:
    logging.error(f"An error occurred in the main execution: {str(e)}")
    print(f"An error occurred: {str(e)}")
    print("Check the 'downloader.log' file for more details.")
