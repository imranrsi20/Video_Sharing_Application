

from django.urls import path
from . import views
from my_video.views import GeneratePDF

urlpatterns = [

        path('',views.video_home,name='home'),
        path('show/<int:id>/',views.play_video,name='show'),
        path('upload_video/',views.upload_video_file,name='upload_video'),
        path('like',views.like_video,name='like_video'),
        path('search/',views.search,name='search'),
        path('history/',views.video_history,name='history'),
        path('draft/',views.draft_video,name='draft'),
        path('published/<int:id>/',views.published_video,name='published'),
        path('play_draft/<int:id>/',views.play_draft_video,name='play_draft'),
        path('history/',views.video_history,name='history'),
        path('watch_later/<int:id>/', views.watch_l, name='watch'),
        path('show_watch/', views.show_watch_later, name='show_watch'),
        path('clear_history/',views.clear_history,name='clear_history'),
        path('clear_watch_later/',views.clear_watch,name='clear_watch_later'),
        path('delete_watch/<int:id>/',views.delete_watch,name='delete_watch'),
        path('pdf/',GeneratePDF.as_view(),name='pdf'),
        path('delete_draft/<int:id>/',views.delete_draft,name='delete_draft'),



]