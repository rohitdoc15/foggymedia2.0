from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from pages.views import inflation_chart_view

urlpatterns = [
    path('', views.home , name='home'),
    path('afterclick/', views.click , name='click'),
    
]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

htmx_url_patterns = [
         path('check_channel/', views.check_channel , name='check_channel'),
         path('searchlist/', views.check_channel , name='searchlist'),
         path('channel/<str:slug>/',views.channel_name, name='channel_name'),
         path('about/',views.click, name='click'),
         path('cloud/',views.cloud, name='cloud'),
         path('apex/',views.apex, name='apex'),
         path('story/<str:channel_name>/', views.story, name='story'),
         path('heatmap/', views.heatmap, name='heatmap'),
         path('fact-check/', views.fact_check, name='fact_check'),
         path('topic-page/', views.topic_page, name='topic_page'),
         path('fact-check-view/', views.fact_check_view, name='fact_check_view'),
         path('topic/<str:topic>/', views.topic_details, name='topic_details'),
         path('inflation-chart-data/', inflation_chart_view, name='inflation-chart-data'),
         path('channels/', views.channel_list, name='channel_list'),
         path('video-count/', views.keyword_video_count, name='video_count'),
         path('popular-person-chart/', views.PopularPersonChartView.as_view(), name='popular_person_chart'),




         




        
]


urlpatterns += htmx_url_patterns