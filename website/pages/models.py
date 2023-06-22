from django.db import models



# Create your models here.

from django.db import models

class NewsChannel(models.Model):
    name = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255,null= True, unique=True)
    tagline = models.CharField(max_length=255, null=True, blank=True)
    politcial_spectrum = models.IntegerField(null=True, blank=True)
    youtube_rank = models.IntegerField(null=True, blank=True)
    fake_news_index = models.IntegerField(null=True, blank=True)
    credibility_index = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    founded_year = models.IntegerField(null=True, blank=True)
    channel_type = models.CharField(max_length=255, null=True, blank=True)
    headquarters = models.CharField(max_length=255, null=True, blank=True)
    owner = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    official_website = models.URLField(null=True, blank=True)
    youtube_channel = models.URLField(null=True, blank=True)
    twitter_handle = models.URLField(max_length=255, null=True, blank=True)
    facebook_page = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to='static/news_logos', null=True, blank=True)
    subscribers = models.CharField(max_length=200,null=True, blank=True)
    facebook_likes = models.CharField(max_length=200,null=True, blank=True)
    twitter_followers = models.CharField(max_length=200,null=True, blank=True)
    
    

    def __str__(self):
        return self.name
    

class TrendingTopic(models.Model):
    topic = models.CharField(max_length=200)
    rank = models.IntegerField(unique=True)
    synopsis = models.TextField(blank=True)

    def __str__(self):
        return self.topic

    class Meta:
        ordering = ['rank']

    @property
    def video_count(self):
        return Video.objects.filter(topic=self.topic).count()    



from django.db.models import Min

class Video(models.Model):
    channel = models.ForeignKey(NewsChannel, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    transcript = models.TextField()
    published_date = models.DateTimeField()
    video_url = models.URLField(max_length=2000)
    thumbnail_url = models.URLField(max_length=2000)
    topic = models.CharField(max_length=255)  # Changed this line
    category = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def first_appearance(self):
        first_date = Video.objects.filter(topic=self.topic).aggregate(Min('published_date'))['published_date__min']
        return first_date



class sarso(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"sarso price: {self.price} on {self.date}"
    

class petroluem(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"petroluem price: {self.price} on {self.date}"      
    

from django.db import models


class TopPopularPersons(models.Model):
    date = models.DateField(unique=True)
    person1_name = models.CharField(max_length=255)
    person1_video_count = models.PositiveIntegerField(null=True)
    person2_name = models.CharField(max_length=255)
    person2_video_count = models.PositiveIntegerField(null=True)
    person3_name = models.CharField(max_length=255)
    person3_video_count = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"Top Popular Persons on {self.date}"

