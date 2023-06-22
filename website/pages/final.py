import sys
sys.path.append('/home/rohit/news/website')
from fuzzywuzzy import fuzz

import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()
from collections import Counter as CollectionsCounter
from pages.models import Video, TrendingTopic

# Get the current time
now = timezone.now()

# Get the time 4 hours ago
time_4_hours_ago = now - timedelta(hours=12)

# Fetch all video topics from your database that were published in the last 4 hours
videos = Video.objects.filter(published_date__range=(time_4_hours_ago, now))

# Get topics from videos
topics = [video.topic for video in videos]

# Calculate the frequency of each topic
topic_counter = CollectionsCounter(topics)

# Filter out blank and dash ("-") topics
for topic in list(topic_counter):
    if topic == "" or topic == "-":
        del topic_counter[topic]

# Stopword list
stopwords = ['India News', 'Top Headlines', 'Viral Videos', 'Gravitas', 'National politics', 'Crime News', 'Hindi News', 'Weather Updates', 'Bihar News', 'R Bharat', 'World News', 'WION Shorts', 'News Events' , 'Delhi fire']

# Expand the stopwords
expanded_stopwords = []
for stopword in stopwords:
    expanded_stopwords.extend(stopword.split())

# Get the 20 most common topics (we get more than 5 because we might discard some topics later)
# Get the 20 most common topics (we get more than 5 because we might discard some topics later)
most_common_topics = topic_counter.most_common(20)
print(f"Most common topics: {most_common_topics}")

# Use fuzzywuzzy to ensure that the most common topics are distinct and not in the stopword list
distinct_topics = []
for topic, _ in most_common_topics:
    if topic not in stopwords:  # Exclude stopwords
        if not distinct_topics:  # if list is empty
            distinct_topics.append(topic)
        else:
            is_distinct = True
            # compare with the topics already in distinct_topics
            for distinct_topic in distinct_topics:
                similarity = fuzz.ratio(topic, distinct_topic)
                # if similarity is greater than 60 or topic contains any stopwords or expanded stopwords, it's not a distinct topic
                if similarity > 40 or any(stopword in topic for stopword in expanded_stopwords):
                    is_distinct = False
                    break
                elif similarity == 40:
                    # Resolve tie by selecting the most recent topic
                    current_topic_videos = Video.objects.filter(topic=topic)
                    distinct_topic_videos = Video.objects.filter(topic=distinct_topic)
                    if current_topic_videos.exists() and distinct_topic_videos.exists():
                        current_topic_latest = current_topic_videos.latest('published_date')
                        distinct_topic_latest = distinct_topic_videos.latest('published_date')
                        if current_topic_latest.published_date > distinct_topic_latest.published_date:
                            distinct_topics.remove(distinct_topic)
                            is_distinct = True
                        else:
                            is_distinct = False
                    elif current_topic_videos.exists():
                        distinct_topics.remove(distinct_topic)
                        is_distinct = True
                    break

            if is_distinct:
                distinct_topics.append(topic)

        if len(distinct_topics) == 5:  # stop if we have 5 distinct topics
            break

# Update the TrendingTopic model
existing_topics = TrendingTopic.objects.all()
existing_topics.delete()  # Delete existing topics

for i, topic in enumerate(distinct_topics):
    trending_topic = TrendingTopic.objects.create(topic=topic, rank=i + 1)
    trending_topic.save()

print(f"Top 5 distinct topics: {distinct_topics}")
