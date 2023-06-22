from django.shortcuts import render
from django.http import HttpResponse , JsonResponse ,FileResponse
from . import templates
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
import html
from fuzzywuzzy import fuzz
from datetime import date
import requests
from operator import itemgetter

from .models import NewsChannel, TrendingTopic,Video
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from django.utils.text import slugify

from django.db.models import Count

from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from django.db.models.functions import TruncDate

from django.db.models import Count
from django.db.models.functions import TruncDate

from datetime import timedelta

def home(request):
    now = timezone.now()

    # Get the time 30 days ago
    time_30_days_ago = now - timedelta(days=30)

    # Get the time 8 hours ago
    time_8_hours_ago = now - timedelta(hours=6)
    time_16_hours_ago = now - timedelta(hours=12)

    news_channels = NewsChannel.objects.all()

    # Fetch all topics in a list
    all_trending_topics = list(TrendingTopic.objects.all())

    # Get the video count for each topic and store it in a dictionary
    topic_info = []
    for topic in all_trending_topics:
        # Only count videos that were published in the last 8 hours
        video_count = Video.objects.filter(topic=topic.topic, published_date__range=(time_8_hours_ago, now)).count()
        topic_info.append({
            'topic': topic,
            'count': video_count,
        })

    # Sort topics based on the video count in descending order
    sorted_topic_info = sorted(topic_info, key=lambda x: x['count'], reverse=True)

    for topic_info in sorted_topic_info:
        topic = topic_info['topic']
        count = topic_info['count']
        previous_8_hours_count = Video.objects.filter(topic=topic.topic, published_date__range=(time_16_hours_ago, time_8_hours_ago)).count()

        if previous_8_hours_count != 0:
            change_percentage = (count - previous_8_hours_count) / previous_8_hours_count * 100
        else:
            change_percentage = 0  # Set a default value or handle it appropriately
        print(count, previous_8_hours_count, change_percentage)
        # Determine the trend indicator based on the change percentage for each topic
        if change_percentage > 30:
            trend_indicator = 'upwards'
        elif change_percentage < -30:
            trend_indicator = 'downwards'
        else:
            trend_indicator = 'normal'
        
        topic_info['trend_indicator'] = trend_indicator
        print(topic_info)

    # Pick the top 5 topics
    top_5_topics = sorted_topic_info[:5]

    # Rest of your code...


    # Calculate top 5 topics from Video model based on video frequency over the last month
    top_5_video_topics_last_month = Video.objects.filter(published_date__range=(time_30_days_ago, now)).values('topic').annotate(count=Count('id')).order_by('-count')[:5]

    # Prepare data for Apex line chart
    chart_data = []
    one_month_ago = timezone.now() - timedelta(days=30)

    # Get top 5 non-empty topics based on video frequency over the past 30 days
    top_topics = Video.objects.filter(published_date__gte=one_month_ago) \
        .exclude(topic='') \
        .values('topic') \
        .annotate(video_count=Count('id')) \
        .order_by('-video_count')[:5]

    # Initialize data dictionary for ApexChart
    data = {
        "series": [],
        "labels": [str(one_month_ago.date() + timedelta(days=i)) for i in range(30)],
        "chart": {
            "height": 350,
            "type": "line"
        },
        "title": {
            "text": 'Video Trend Over the Past 30 Days'
        },
        "xaxis": {
            "categories": [str(one_month_ago.date() + timedelta(days=i)) for i in range(30)]
        },
    }
    # Calculate the latest video timestamp
    latest_video_timestamp = Video.objects.latest('published_date').published_date

    # For each of the top 5 topics, get the daily video count for the past 30 days
    for topic in top_topics:
        video_count_per_day = []
        for i in range(30):
            date = one_month_ago + timedelta(days=i)
            video_count = Video.objects.filter(topic=topic['topic'], published_date__date=date).count()
            video_count_per_day.append(video_count)

        # Append this topic's data to the series list
        data["series"].append({
            "name": topic['topic'],
            "data": video_count_per_day
        })

    context = {
        'channels': news_channels,
        'topic1': top_5_topics[0],
        'topic2': top_5_topics[1],
        'topic3': top_5_topics[2],
        'topic4': top_5_topics[3],
        'topic5': top_5_topics[4],
        'data': data,
        'latest_video_timestamp': latest_video_timestamp,
    }

    print(data)


    return render(request, 'pages/home.html', context)

import json
from django.http import JsonResponse
from pages.models import sarso , petroluem

def inflation_chart_view(request):
    sarso_data = sarso.objects.values('date', 'price')
    petroluem_data = petroluem.objects.values('date', 'price')
    
    sarso_chart_data = [{'x': item['date'].strftime('%Y-%m-%d'), 'y': item['price']} for item in sarso_data]
    petroluem_chart_data = [{'x': item['date'].strftime('%Y-%m-%d'), 'y': item['price']} for item in petroluem_data]
    
    chart_data = [
        {'name': 'Sarso', 'data': sarso_chart_data},
        {'name': 'Petroluem', 'data': petroluem_chart_data}
    ]
    
    print(chart_data)
    return JsonResponse({'chart_data': chart_data})






def click(request):
    result = request.POST.get('name')
    print(result)
    context = {'results': result}
    return render(request, 'pages/afterclick.html',context)




from django.db import models



from django.http import JsonResponse

from django.db.models import Q



from django.http import JsonResponse

from django.urls import reverse
from django.http import JsonResponse

# def check_channel(request):
#     query = request.POST.get('search', '').strip()

#     if not query:
#         return JsonResponse({'results': []})

#     channel_results = NewsChannel.objects.filter(name__icontains=query)
#     topic_results = Video.objects.filter(topic__icontains=query).values('topic').annotate(video_count=models.Count('id')).filter(video_count__gt=50)

#     results_list = []
#     counter = 0  # Counter to track the number of results

from django.db.models import Count

def check_channel(request):
    query = request.POST.get('search', '').strip()

    if not query:
        return JsonResponse({'results': []})

    channel_results = NewsChannel.objects.filter(name__icontains=query)
    topic_results = Video.objects.filter(topic__icontains=query).values('topic').annotate(video_count=Count('id')).filter(video_count__gt=50)

    results_list = []
    counter = 0  # Counter to track the number of results

    for channel in channel_results:
        if counter >= 5:  # Break out of the loop once the limit is reached
            break

        result_dict = {
            'name': channel.name,
            'slug': channel.slug,
            'logo': channel.logo.url if channel.logo else None,  # Add the logo URL to the result dictionary
            'topics': [],
        }
        results_list.append(result_dict)
        counter += 1  # Increment the counter

    for topic in topic_results:
        if counter >= 5:  # Break out of the loop once the limit is reached
            break

        topic_data = {
            'topic': topic['topic'],
            'video_count': topic['video_count'],
        }
        results_list.append({'name': '', 'slug': '', 'logo': None, 'topics': [topic_data]})

        counter += 1  # Increment the counter
    print(results_list)    

    return JsonResponse({'results': results_list})



from django.shortcuts import render


from django.shortcuts import render
from .models import Video

from django.db.models import Min

from django.core.paginator import Paginator








from django.core.serializers.json import DjangoJSONEncoder
import json

from django.utils import formats

import operator
from datetime import datetime, timedelta
from django.utils import formats

from datetime import datetime, timedelta
from django.utils import formats
from django.db.models import Count,Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def channel_name(request, slug):
    news_channel = NewsChannel.objects.get(slug=slug)

    # Get the videos related to this channel
    videos = Video.objects.filter(channel=news_channel)

    # Filter videos from the past day and exclude blank or empty titles
    one_day_ago = datetime.now() - timedelta(days=1)
    day_videos = videos.filter(published_date__gte=one_day_ago).exclude(title__isnull=True).exclude(title='')

    # Get the count of each topic
    topic_counts = list(day_videos.values('topic').annotate(topic_count=Count('topic')).order_by('-topic_count'))

    # Decode HTML entities in topics and exclude null or empty topics
    topic_counts = [tc for tc in topic_counts if tc['topic']]
    
    # Merge duplicate topics and get the top five topics
    top_five_topics = merge_duplicate_topics(topic_counts)

    # Filter videos from the past week and exclude blank or empty titles for Modi and Rahul Gandhi count
    one_week_ago = datetime.now() - timedelta(weeks=1)  # Change the timedelta to 1 week
    week_videos = videos.filter(published_date__gte=one_week_ago).exclude(title__isnull=True).exclude(title='')
    
    # Define the religious terms
    religious_terms = ["हिन्दू", "मुस्लिम",]  # Replace with your actual religious terms

    # Count daily occurrences of "Modi", "Rahul Gandhi", and religious terms in the past week and compute percentages
    historical_counts = {}
    today = date.today()
    for i in range(7):
        current_date = today - timedelta(days=6 - i)  # Reverse the range
        total_videos = week_videos.filter(published_date__date=current_date).count()
        count_modi = week_videos.filter(published_date__date=current_date, title__icontains='Modi').count()
        count_rahul = week_videos.filter(published_date__date=current_date, title__icontains='Rahul Gandhi').count()
        count_religious = week_videos.filter(published_date__date=current_date, title__iregex=r'|'.join(religious_terms)).count()  # Use iregex to match any religious term
        formatted_date = current_date.strftime("%d %B")  # Format the date
        religious_percentage = round((count_religious / total_videos) * 100) if total_videos else 0  # Calculate religious term percentage
        historical_counts[formatted_date] = {
            "Modi": round((count_modi / total_videos) * 100) if total_videos else 0,
            "Rahul Gandhi": round((count_rahul / total_videos) * 100) if total_videos else 0,
            "Religious": religious_percentage  # Add religious percentage to historical_counts
            
        }
    upload_frequency = [week_videos.filter(published_date__date=current_date).count() for current_date in [today - timedelta(days=i) for i in range(6, -1, -1)]]

    # Videos pagination
    videos_list = videos.order_by('-published_date')
    page = request.GET.get('page', 1)  # Get the page number from the query string
    paginator = Paginator(videos_list, 5)  # Show 5 videos per page

    try:
        paginated_videos = paginator.page(page)
    except PageNotAnInteger:
        paginated_videos = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:
        paginated_videos = paginator.page(paginator.num_pages)  # If page is out of range, deliver last page of results.

    context = {
        "channel": news_channel,
        "topic_counts": top_five_topics,
        "historical_counts": json.dumps(historical_counts, cls=DjangoJSONEncoder),
        "upload_frequency": upload_frequency,
        "videos": paginated_videos  # Pass paginated videos to context
    }

    return render(request, 'pages/channelname.html', context)








def merge_duplicate_topics(topic_counts):
    merged_topics = []

    for topic1 in topic_counts:
        topic_count = topic1['topic_count']
        merged_topic = topic1['topic']
        duplicate_found = False

        for topic2 in merged_topics:
            ratio = fuzz.token_sort_ratio(topic1['topic'], topic2['topic'])
            if ratio > 50:
                merged_topic = shorter_string(merged_topic, topic2['topic'])
                topic_count += topic2['topic_count']
                duplicate_found = True

        if not duplicate_found:
            merged_topics.append({'topic': merged_topic, 'topic_count': topic_count})

    merged_topics.sort(key=lambda x: x['topic_count'], reverse=True)

    return merged_topics[:5]


def shorter_string(str1, str2):
    return str1 if len(str1) <= len(str2) else str2




def cloud(request):
    result = request.POST.get('name')
    print(result)
    context = {'results': result}
    return render(request, 'pages/cloud.html',context)

from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from .models import TrendingTopic, Video

from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from .models import TrendingTopic, Video

from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Video

def apex(request):
    # Date 30 days ago from now
    one_month_ago = timezone.now() - timedelta(days=30)

    # Get top 5 topics based on video frequency over the past 30 days
    top_topics = Video.objects.filter(published_date__gte=one_month_ago)\
        .values('topic')\
        .annotate(video_count=Count('id'))\
        .order_by('-video_count')[:5]

    # Initialize data dictionary for ApexChart
    data = {
        "series": [],
        "labels": [str(one_month_ago.date() + timedelta(days=i)) for i in range(30)],
        "chart": {
            "height": 350,
            "type": "line"
        },
        "title": {
            "text": 'Video Trend Over the Past 30 Days'
        },
        "xaxis": {
            "categories": [str(one_month_ago.date() + timedelta(days=i)) for i in range(30)]
        },
    }

    # For each of the top 5 topics, get the daily video count for the past 30 days
    for topic in top_topics:
        video_count_per_day = []
        for i in range(30):
            date = one_month_ago + timedelta(days=i)
            video_count = Video.objects.filter(topic=topic['topic'], published_date__date=date).count()
            video_count_per_day.append(video_count)

        # Append this topic's data to the series list
        data["series"].append({
            "name": topic['topic'],
            "data": video_count_per_day
        })
        print(data)

    return render(request, 'pages/apex.html', {'data': data})


def story(request, channel_name):
    news_channel = get_object_or_404(NewsChannel, name=channel_name)
    all_channels = NewsChannel.objects.all()
    context = {'channel': news_channel, 'channels': all_channels}
    return render(request, 'pages/story.html', context)




from django.shortcuts import render
import json

from django.db.models import Count
from pages.models import Video

def heatmap(request):
    # Get a list of topics that have more than 50 videos associated with them
    # Original queryset
    topics = Video.objects.values('topic').annotate(video_count=Count('topic')).filter(video_count__gt=50)

    # Transformation
    heatmap_data = []
    for topic in topics:
        heatmap_dict = {}
        # For example, we map the first character of the topic to a day in the month
        heatmap_dict['day'] = ord(topic['topic'][0]) % 31 + 1
        # And we map the video count to an hour in the day
        heatmap_dict['hour'] = topic['video_count'] % 24
        # And we use the video count as the count (you could use a different property here if you prefer)
        heatmap_dict['count'] = topic['video_count']
        heatmap_data.append(heatmap_dict)

    return render(request, 'pages/heatmap.html', {'topics': heatmap_data})



import requests
from django.shortcuts import render

def fact_check(request, search_term=None, return_results=False):
    if not search_term:
        search_term = request.GET.get('search_term', '')  # Get the search term from the request

    if search_term:
        # Perform the fact check API request
        api_key = 'AIzaSyB9BgMqW9AXGQD0ZfHWgFrtq6tTz9WEUVo'  # Replace with your actual API key
        url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?key={api_key}"
        params = {
            'query': search_term,
            'pageSize': 10,
            'languageCode': 'en',
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            fact_checks = data.get('claims', [])

            if return_results:
                # If the return_results argument is True, return the fact checks as a list
                return fact_checks

            # Otherwise, render the template with the fact checks, search term, and error message (if any)
            context = {
                'fact_checks': fact_checks,
                'search_term': search_term,
                'error_message': None,
            }
            return render(request, 'pages/factcheck.html', context)
        except requests.exceptions.RequestException as e:
            error_message = f"Error occurred: {str(e)}"
            context = {
                'fact_checks': [],
                'search_term': search_term,
                'error_message': error_message,
            }
            return render(request, 'pages/factcheck.html', context)

    # Render the template with the search form
    return render(request, 'pages/factcheck.html')


from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def fact_check_view(request):
    search_term = request.GET.get('search_term', '')
    fact_checks = fact_check(request, search_term, return_results=True)
    print(fact_checks)
    return JsonResponse({'fact_checks': fact_checks[:5]})





from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

from django.shortcuts import render

from datetime import datetime, timedelta

from django.shortcuts import render
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import NewsChannel, Video, TrendingTopic
import json

@csrf_exempt
def topic_page(request):
    if request.method == 'POST':
        topic = request.POST.get('topic', '')
        top_channels = NewsChannel.objects.annotate(video_count=Count('videos', filter=Q(videos__topic=topic))).order_by('-video_count')[:5]

        # Retrieve the synopsis for the topic
        try:
            trending_topic = TrendingTopic.objects.get(topic=topic)
            synopsis = trending_topic.synopsis
        except TrendingTopic.DoesNotExist:
            synopsis = ""

        # Retrieve the last video for the topic
        last_video = Video.objects.filter(topic=topic).order_by('-published_date').first()
        last_video_thumbnail_url = last_video.thumbnail_url if last_video else None

        # Count the videos for the topic
        video_count = Video.objects.filter(topic=topic).count()

        # Get the first video for the topic
        first_video = Video.objects.filter(topic=topic).order_by('published_date').first()
        first_appeared_date = first_video.published_date if first_video else None

        # Count the videos for the last seven days
        today = datetime.now().date()
        seven_days_ago = today - timedelta(days=6)
        daily_counts = []
        day_labels = []
        for i in range(7):
            current_date = seven_days_ago + timedelta(days=i)
            count = Video.objects.filter(topic=topic, published_date__date=current_date).count()
            daily_counts.append(count)
            day_labels.append(current_date.strftime("%b %d"))  # Add formatted day labels

        # Get the latest 5 videos
        latest_videos = Video.objects.filter(topic=topic).order_by('-published_date')[:5]

        context = {
            'title': topic,
            'top_channels': top_channels,
            'synopsis': synopsis,
            'last_video_thumbnail_url': last_video_thumbnail_url,
            'topic_count': video_count,
            'first_appeared_date': first_appeared_date,
            'daily_counts': daily_counts,
            'daily_counts_json': json.dumps(daily_counts),  # Convert daily_counts to JSON
            'day_labels': day_labels,  # Pass day labels to template
            'latest_videos': latest_videos,
        }

        return render(request, 'pages/topic_page.html', context)
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=400)
from functools import reduce


from django.shortcuts import render
from django.db.models import Q

def topic_details(request, topic=None):
    if request.method == 'POST':
        if topic is None:
            topic = request.POST.get('topic', '')
    elif request.method == 'GET':
        if topic is None:
            topic = request.GET.get('topic', '')
    else:
        return JsonResponse({"error": "Only GET and POST methods are allowed."}, status=400)

    top_channels = NewsChannel.objects.annotate(video_count=Count('videos', filter=Q(videos__topic=topic))).order_by('-video_count')[:5]

    # Retrieve the synopsis for the topic
    try:
        trending_topic = TrendingTopic.objects.get(topic=topic)
        synopsis = trending_topic.synopsis
    except TrendingTopic.DoesNotExist:
        synopsis = ""

    # Retrieve the last video for the topic
    last_video = Video.objects.filter(topic=topic).order_by('-published_date').first()
    last_video_thumbnail_url = last_video.thumbnail_url if last_video else None

    # Count the videos for the topic
    video_count = Video.objects.filter(topic=topic).count()

    # Get the first video for the topic
    first_video = Video.objects.filter(topic=topic).order_by('published_date').first()
    first_appeared_date = first_video.published_date if first_video else None

    # Get all-time historical daily counts
    all_time_counts = Video.objects.filter(topic=topic).values('published_date__date').annotate(count=Count('id')).order_by('published_date__date')
    daily_counts = [entry['count'] for entry in all_time_counts]
    day_labels = [entry['published_date__date'].strftime("%b %d") for entry in all_time_counts]

    # Get the latest 5 videos
    latest_videos = Video.objects.filter(topic=topic).order_by('-published_date')[:5]

    # Split the topic into individual words
    topic_words = topic.split()

    # Get related topics based on matching words and more than 50 videos
    related_topics = Video.objects.filter(
        reduce(lambda x, y: x | y, [Q(topic__icontains=word) for word in topic_words])
    ).exclude(topic=topic).values('topic').annotate(video_count=Count('id')).filter(video_count__gt=50).order_by('-video_count')[:3]

    context = {
        'title': topic,
        'top_channels': top_channels,
        'synopsis': synopsis,
        'last_video_thumbnail_url': last_video_thumbnail_url,
        'topic_count': video_count,
        'first_appeared_date': first_appeared_date,
        'daily_counts': daily_counts,
        'daily_counts_json': json.dumps(daily_counts),  # Convert daily_counts to JSON
        'day_labels': day_labels,  # Pass day labels to template
        'latest_videos': latest_videos,
        'related_topics': related_topics,
    }
    print(related_topics   )

    return render(request, 'pages/topic_details.html', context)



from django.shortcuts import render
from django.db.models import Count, Avg

from django.db.models import Count, F, FloatField, ExpressionWrapper
from datetime import datetime, timedelta

from django.db.models import Count, F, FloatField, ExpressionWrapper
from datetime import datetime, timedelta

from django.db.models import Count, F, FloatField, ExpressionWrapper
from datetime import datetime, timedelta

def channel_list(request):
    seven_days_ago = datetime.now() - timedelta(days=7)
    channels = NewsChannel.objects.annotate(video_count=Count('videos')).order_by('youtube_rank')

    for channel in channels:
        videos_per_day = Video.objects.filter(
            channel=channel,
            published_date__gte=seven_days_ago
        ).count() / 7
        channel.avg_videos_per_day = round(videos_per_day, )

        channel.fake_news_rating = channel.fake_news_index
        channel.credibility = channel.credibility_index

    context = {
        'channels': channels
    }

    return render(request, 'pages/channel_list.html', context)


from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from .models import NewsChannel, Video

def channel_list(request):
    seven_days_ago = datetime.now() - timedelta(days=7)
    channels = NewsChannel.objects.annotate(video_count=Count('videos')).order_by('youtube_rank')

    for channel in channels:
        videos_per_day = Video.objects.filter(
            channel=channel,
            published_date__gte=seven_days_ago
        ).count() / 7
        channel.avg_videos_per_day = round(videos_per_day)

        channel.fake_news_rating = channel.fake_news_index
        channel.credibility = channel.credibility_index

    context = {
        'channels': channels
    }

    return render(request, 'pages/channel_list.html', context)


def keyword_video_count(request):
    bjp_keywords = [
        'modi', 'bjp', 'narendra modi',  # English keywords
        'मोदी', 'भाजपा', 'नरेंद्र मोदी'  # Hindi keywords
    ]

    aap_keywords = [
        'kejriwal', 'aam admi party', 'arvind kejriwal', 'manish sisodia'  # English keywords
        'केजरीवाल', 'आम आदमी पार्टी', 'अरविंद केजरीवाल'  # Hindi keywords
    ]

    congress_keywords = [
        'rahul gandhi', 'congress', 'sonia gandhi',  # English keywords
        'राहुल गांधी', 'कांग्रेस', 'सोनिया गांधी'  # Hindi keywords
    ]

    shivsena_keywords = [
        'uddhav thackeray', 'shiv sena', 'aditya thackeray',  # English keywords
        'उद्धव ठाकरे', 'शिवसेना', 'आदित्य ठाकरे'  # Hindi keywords
    ]

    tmc_keywords = [
        'mamata banerjee', 'trinamool congress', 'abhishek banerjee', 'TMC', # English keywords
        'ममता बनर्जी', 'तृणमूल कांग्रेस', 'अभिषेक बनर्जी'  # Hindi keywords
    ]

    sp_keywords = [
        'mulayam singh yadav', 'samajwadi party', 'akilesh yadav',  # English keywords
        'मुलायम सिंह यादव', 'समाजवादी पार्टी', 'अखिलेश यादव'  # Hindi keywords
    ]

    # Combine all the keywords into a single list
    all_keywords = bjp_keywords + aap_keywords + congress_keywords + shivsena_keywords + tmc_keywords + sp_keywords

    # Get the last 2 days' news videos
    two_days_ago = timezone.now() - timezone.timedelta(days=2)
    news_videos = Video.objects.filter(published_date__gte=two_days_ago)

    # Get all news channels
    news_channels = NewsChannel.objects.all()
    total_videos = 0

    # Initialize the dictionary to store the party scores
    party_scores = {
        'BJP': 0,
        'AAP': 0,
        'Congress': 0,
        'Shiv Sena': 0,
        'Trinamool Congress': 0,
        'Samajwadi Party': 0
    }

    # Iterate through the news titles and calculate the scores for each party
    for video in news_videos:
        title = video.title.lower()

        # Initialize the flag to check if any party keyword is found
        party_found = False

        # Check for BJP keywords
        for keyword in bjp_keywords:
            if keyword in title:
                party_scores['BJP'] += 1
                party_found = True
                break

        # Check for AAP keywords
        for keyword in aap_keywords:
            if keyword in title:
                party_scores['AAP'] += 1
                party_found = True
                break

        # Check for Congress keywords
        for keyword in congress_keywords:
            if keyword in title:
                party_scores['Congress'] += 1
                party_found = True
                break

        # Check for Shiv Sena keywords
        for keyword in shivsena_keywords:
            if keyword in title:
                party_scores['Shiv Sena'] += 1
                party_found = True
                break

        # Check for Trinamool Congress keywords
        for keyword in tmc_keywords:
            if keyword in title:
                party_scores['Trinamool Congress'] += 1
                party_found = True
                break

        # Check for Samajwadi Party keywords
        for keyword in sp_keywords:
            if keyword in title:
                party_scores['Samajwadi Party'] += 1
                party_found = True
                break


        if party_found:

            for party, keywords in zip(party_scores.keys(), [bjp_keywords, aap_keywords, congress_keywords,
                                                             shivsena_keywords, tmc_keywords, sp_keywords]):
                if any(keyword in title for keyword in keywords):
                    print( end=" ")
            
        if party_found:
            total_videos += 1
    

 
    print(f"Total videos: {total_videos}")       

    # Return the JSON response with the party scores
    return JsonResponse(party_scores)



from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from datetime import timedelta
from .models import TopPopularPersons
from django.views.generic import View
from django.http import JsonResponse
from .models import TopPopularPersons

class PopularPersonChartView(View):
    def get(self, request):
        data = {
            'chart': {'type': 'line'},
            'series': [{'name': 'Popular Person', 'data': []}],
            'xaxis': {'categories': []}
        }

        # Retrieve the last 20 days' data
        top_persons = TopPopularPersons.objects.order_by('-date')[:20]

        # Populate the chart data
        for person in top_persons:
            person_data = f"{person.person1_name} ({person.person1_video_count})"
            data['series'][0]['data'].append(person_data)
            data['xaxis']['categories'].append(str(person.date))

       
        return JsonResponse(data)
