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


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
from datetime import datetime
from pages.models import petroluem

# data = [
#     {'date': datetime(2022, 1, 1), 'price': 94},
#     {'date': datetime(2022, 2, 1), 'price': 104},
#     {'date': datetime(2022, 3, 1), 'price': 103},
#     {'date': datetime(2022, 4, 1), 'price': 103},
#     {'date': datetime(2022, 5, 1), 'price': 103},
#     {'date': datetime(2022, 6, 1), 'price': 103},
#     {'date': datetime(2022, 7, 1), 'price': 103},
#     {'date': datetime(2023, 1, 1), 'price': 103},
#     {'date': datetime(2023, 2, 1), 'price': 103},
#     {'date': datetime(2023, 3, 1), 'price': 103},
#     {'date': datetime(2023, 4, 1), 'price': 103},
#     {'date': datetime(2023, 5, 1), 'price': 103},
#     {'date': datetime(2023, 6, 1), 'price': 103},
# ]

# # Clear existing data
# petroluem.objects.all().delete()

# # Create new instances and save them
# for item in data:
#     petroluem_instance = petroluem(price=item['price'], date=item['date'])
#     petroluem_instance.save()


# #replace a topic with another topic
# from datetime import datetime, timedelta
# from django.utils import timezone

# old_topic = "Twitter Controversy "
# new_topic = "Adipurush  Controversy"

# # Calculate the datetime from 24 hours ago
# twenty_four_hours_ago = timezone.now() - timedelta(hours=48)

# # Select the videos with the old topic published within the last 24 hours and update their topic field
# updated_videos_count = Video.objects.filter(topic=old_topic, published_date__gte=twenty_four_hours_ago).update(topic=new_topic)

# print(f"Updated {updated_videos_count} videos.")


from datetime import date
from pages.models import PopularPerson

desired_date = date(2023, 6, 20)  # Replace with your desired date

# Query the PopularPerson model for the desired date
popular_persons = PopularPerson.objects.filter(dates__date=desired_date)

# Check if any popular person exists on the desired date
if popular_persons.exists():
    print("Popular person(s) exist on the desired date.")
    for person in popular_persons:
        print(person.name)
else:
    print("No popular person exists on the desired date.")
