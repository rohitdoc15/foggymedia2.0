import sys
import time
sys.path.append('/home/rohit/news/website')
from googletrans import Translator
translator = Translator()
import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')  
django.setup()
from collections import Counter as CollectionsCounter
from pages.models import NewsChannel, Video, TrendingTopic

import sys
import os
import django
import PIL.Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import datetime
import matplotlib.cbook as cbook
import matplotlib.image as image
from django.utils import timezone
from pages.models import NewsChannel, Video


# Get the current time and define the time threshold
current_time = timezone.now()
time_threshold = current_time - datetime.timedelta(hours=48)

def generate_word_cloud(channel):
    # Get the videos for the channel published within the time threshold
    videos = Video.objects.filter(channel=channel, published_date__gte=time_threshold)
    titles = [video.title for video in videos]

    # Join the titles to create the text data
    text = ' '.join(titles)

    # Read the stop words from a file
    with open('website/static/function/stop.txt', 'r', encoding='utf8') as stop_file:
        stop_words = stop_file.read().split()

    # Split the text into words
    words = text.split()

    # Count the frequency of each word
    freq_list = Counter(words)

    # Remove the stop words from the frequency list
    for word in stop_words:
        freq_list.pop(word, None)

    # Create a dictionary from the frequency list
    word_freq = dict(freq_list)

    # Load the mask image
    python_mask = np.array(PIL.Image.open(f"website/static/function/logos/{channel}.jpg"))
    colormap = ImageColorGenerator(python_mask)

    # Generate the word cloud
    wordcloud = WordCloud(font_path='website/static/function/Arya-Regular.ttf',
                          mask=python_mask,
                          min_word_length=200,
                          background_color=None,
                          max_words=400,
                          stopwords=set(list(STOPWORDS) + stop_words),
                          min_font_size=5).generate_from_frequencies(word_freq)
    wordcloud.recolor(color_func=colormap)

    # Plot the word cloud
    fig = plt.figure(figsize=(10, 10), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    # Save the word cloud as SVG
    svg_image = wordcloud.to_svg(embed_font=True)
    with open(f"website/static/function/clouds/{channel}.svg", "w+", encoding='UTF-8') as f:
        f.write(svg_image)

    # Add the footer image to the plot
    # with cbook.get_sample_data('website/static/function/footerw.png') as file:
    #     im = image.imread(file)
    # fig.figimage(im, 1, 1, zorder=0, alpha=1)

    # Set the text color and add channel information
    COLOR = 'white'
    plt.rcParams['text.color'] = COLOR
    plt.text(10, 980, f"Channel: {channel.name} ")

    # Save the plot as a PNG image
    png_image = plt.savefig(f"website/static/function/clouds/png/{channel}.png")

# Get all NewsChannel objects
channels = NewsChannel.objects.all()

# Loop through the channels and generate word clouds
for channel in channels:
    generate_word_cloud(channel)
