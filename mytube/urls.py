"""mytube URL Configuration

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
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import password_reset,password_reset_done,password_reset_confirm,password_reset_complete
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('my_video.urls')),

    path('',include('Register_Account.urls')),

    path('', include('django.contrib.auth.urls')),
    path('password_reset/', password_reset,name='password_reset'),
    # url('password_reset/', auth_views.password_reset, {'template_name': 'accounts/reset_password.html'}),
    path('password_reset/done/', password_reset_done),
    path('reset/<uidb64>/<token>', password_reset_confirm),
    path('reset/done/', password_reset_complete),



    path('ckeditor/', include('ckeditor_uploader.urls')),


]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

