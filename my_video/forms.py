from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class U_video(forms.ModelForm):
    class Meta:
        model=video_upload
        fields=[
            "video_title",
            "video_cover_page",
            "your_video",
            "category",
            "short_description"

        ]

class commentForm(forms.ModelForm):
    video_comment = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Add a Public Comment..."}), required=True,
                                   max_length=1000)
    class Meta:
        model=comment
        fields=[
            "video_comment"
        ]



