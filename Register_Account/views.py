from django.shortcuts import render,HttpResponse,get_object_or_404,redirect,Http404
from django.contrib.auth import authenticate,login,logout
from .forms import*
from  django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from my_video .models import *
from django.db.models import Q
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .token import account_activation_token
from my_video.models import video_upload


def signup(request):
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_active = False
            instance.save()
            site = get_current_site(request)
            mail_subject = "confirmation message for MyTube."
            message = render_to_string('confirm_email.html', {

                "user": instance,
                "domain": site.domain,
                "uid": instance.id,
                "token": account_activation_token.make_token(instance)

            })
            to_email = form.cleaned_data.get('email')
            to_list = [to_email]
            from_email = settings.EMAIL_HOST_USER
            send_mail(mail_subject, message, from_email, to_list, fail_silently=True)

            return HttpResponse("<h1>Thanks for your Registrations. A confirmation link was sent to your email.</h1>")

        return render(request, 'signup.html', {"form": form})



def activate(request,uid,token):
    try:
        user=get_object_or_404(User,pk=uid)
    except:
        raise Http404("No User Found.")

    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        c_email=user.email
        group_email.objects.create(u_email=c_email)
        return HttpResponse("<h1>Account is activated. Now you can <a href='/sign-in'>Login</a></h1>")
    else:
        return HttpResponse('Activation link is invalid!')




def getsignin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            user = request.POST.get('user')
            password = request.POST.get('pass')

            auth = authenticate(request, username=user, password=password)

            if auth is not None:
                login(request, auth)
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR, 'username or password is incorrect.')
                return redirect('sign-in')
    return render(request,'sign-in.html')


def getlogout(request):
    logout(request)
    return redirect('sign-in')



def channel(request):
    form = C_channel(request.POST or None, request.FILES or None)
    user_e = get_object_or_404(User, id=request.user.id)
    name = get_object_or_404(User, id=request.user.id)
    f_name = name.first_name
    first_latter = f_name[0]

    if form.is_valid():
        instance=form.save(commit=False)
        instance.author_name=user_e
        instance.save()
        return redirect('upload_video')
    return render(request,'create_channel.html',{"form":form,"first_letter": first_latter})



def view_channel(request,id):
    v = get_object_or_404(video_upload, pk=id)
    all_video=video_upload.objects.filter(uploader_name=v.uploader_name).order_by('-id')

    context={
        "channel":v,
        "all_video":all_video,
    }


    return render(request,'channel_view.html',context)


def author_all_video(request):
    authoruser = get_object_or_404(author, author_name=request.user.id)

    all_video = video_upload.objects.filter(uploader_name=authoruser.id)


    context={
        "channel_name":authoruser,

        "all_video":all_video,
    }

    return render(request,'show_all_video.html',context)

def profile_view(request):
    return render(request,'sample.html')


def Account_view(request):
    return render(request,'account.html')

def group_email_view(request):
    all_email=group_email.objects.all()
    return render(request,'group_email.html',{"email":all_email})

def sent_email(request):
    if request.method=="POST":
        subject=request.POST['subject']
        body=request.POST['body']

        to_email=group_email.objects.all()
        li=[]
        for to in to_email:
            li.append(str(to))
        send_mail(subject,body,'imranhossainrsi2015@gmail.com',li,fail_silently=False,)

    return render(request,'send_email.html')


def view_profile(request):
    profile=author.objects.filter(id=request.user.id)
    for profile in profile:
        print(profile.author_name.first_name)
    context={
        "profile":profile,
    }
    return render(request,'view_profile.html',context)