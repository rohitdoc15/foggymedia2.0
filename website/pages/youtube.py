import sys
sys.path.append('/home/rohit/news/website')

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')  # replace my_project with your project name
django.setup()

from googleapiclient.discovery import build
from pages.models import NewsChannel, Video  # replace your_app_name with the actual name of your Django app

api_key = "AIzaSyCj03npWHxB9EN64MqhiuRTOHMQyIWK7DU"
youtube = build('youtube', 'v3', developerKey=api_key)

def update(channel):
    channel_id = channel.channel_id
    request = youtube.search().list(part="snippet", channelId=channel_id, order='date', maxResults=200)
    response = request.execute()

    for item in response['items']:
        if item['id']['kind'] == "youtube#video":
            thumbnail_url = item['snippet']['thumbnails']['default']['url']
            hq_thumbnail_url = thumbnail_url.replace('/default.jpg', '/hqdefault.jpg')
            
            video, created = Video.objects.get_or_create(
                channel=channel,
                title=item['snippet']['title'],
                video_url=f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                defaults={
                    'thumbnail_url': hq_thumbnail_url,
                    'published_date': item['snippet']['publishedAt'],
                    # Add additional fields as necessary
                }
            )


news_channels = NewsChannel.objects.all()

for channel in news_channels:
    try:
        update(channel)
    except Exception as e:
        print('error in', channel.name, e)
