"""djangoblock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [

        path('signup/',views.signup,name='signup'),
        path('create_channel/',views.channel,name='create_channel'),
        path('sign-in/',views.getsignin,name='sign-in'),
        path('logout/',views.getlogout,name='logout'),
        path('channel/<int:id>/',views.view_channel,name='channel'),
        path('activate/<uid>/<token>', views.activate, name='activate'),
        path('accounts/profile/', views.profile_view,name='accounts/profile'),
        path('account/',views.Account_view,name='account'),
        path('group_email/',views.group_email_view,name='group_email'),
        path('sent_email/',views.sent_email,name='sent_email'),
        path('show_all_video/',views.author_all_video,name='show_all_video'),
        path('view_profile/',views.view_profile,name='view_profile'),

]
