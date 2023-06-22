from django.contrib import admin

from .models import NewsChannel, TrendingTopic , Video , sarso, petroluem ,TopPopularPersons

admin.site.register(NewsChannel)
admin.site.register(TrendingTopic)
admin.site.register(Video)
admin.site.register(sarso)
admin.site.register(petroluem)
admin.site.register(TopPopularPersons)  
