from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(video_category)
admin.site.register(video_upload)
admin.site.register(comment)
admin.site.register(user_ip)
admin.site.register(history)
admin.site.register(watch_later)