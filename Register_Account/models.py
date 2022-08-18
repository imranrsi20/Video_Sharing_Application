from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class author(models.Model):
    author_name=models.ForeignKey(User,on_delete=models.CASCADE)
    channel_name=models.CharField(max_length=300)
    channel_background_image=models.FileField(upload_to='channel_background_image/', blank=True)
    profile_picture=models.FileField(upload_to='profile_picture/',blank=True)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.channel_name


class group_email(models.Model):
    u_email=models.EmailField()
    e_activate=models.BooleanField(default=False)

    def __str__(self):
        return self.u_email