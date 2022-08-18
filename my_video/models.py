from django.db import models
from Register_Account.models import author
from django.contrib.auth.models import User



class video_category(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name




class video_upload(models.Model):
    uploader_name=models.ForeignKey(author,on_delete=models.CASCADE)
    video_title=models.CharField(max_length=1000)
    video_cover_page=models.FileField(upload_to='cover_photo/')
    your_video=models.FileField(upload_to='uploaded_video/')
    category=models.ForeignKey(video_category,on_delete=models.CASCADE,blank=True,default=True)
    short_description=models.TextField()
    likes=models.ManyToManyField(User,related_name='likes',blank=True)
    published_day=models.DateTimeField(auto_now_add=True)
    is_delete=models.BooleanField(default=False)
    draft=models.BooleanField(default=False)

    def __str__(self):
        return self.video_title

    def total_likes(self):
        return self.likes.count()

class user_ip(models.Model):
    ip=models.CharField(max_length=20)
    video=models.ForeignKey(video_upload,on_delete=models.CASCADE,default=True)

    def __str__(self):
        return self.ip



class comment(models.Model):
    post=models.ForeignKey(video_upload,on_delete=models.CASCADE)
    commented_name=models.ForeignKey(author,on_delete=models.CASCADE)
    video_comment=models.CharField(max_length=1000)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.video_title




class history(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    v_id=models.IntegerField()


    def __str__(self):
        return str(self.v_id)


class watch_later(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    v_id=models.IntegerField()


    def __str__(self):
        return str(self.v_id)