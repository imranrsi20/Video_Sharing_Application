from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from Register_Account.models import author
from django.contrib import messages
from django.template.loader import render_to_string
from .models import *
from .forms import *
from django.db.models import Q
from django.http import HttpRequest
from django.contrib.auth.models import User
import itertools
import random
from django.core.mail import send_mail


from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from my_video.utils import render_to_pdf #created in step 4





class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('invoice.html')
        context = {
            "invoice_id": 123,
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
        }
        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")







def draft_video(request):
    all_video=video_upload.objects.filter(draft=False).order_by('-id')
    user = get_object_or_404(User, id=request.user.id)

    user_p = author.objects.filter(author_name=user.id)
    if user_p:
        u = get_object_or_404(author, author_name=user.id)
        context = {
            "video": all_video,
            "user_profile": u,
        }
        return render(request, 'draft.html', context)
    else:
        name = get_object_or_404(User, id=request.user.id)
        f_name = name.first_name
        first_latter = f_name[0]

        context = {
            "video": all_video,
            "first_letter": first_latter,

        }
        return render(request, 'draft.html', context)


def play_draft_video(request,id):
    all_video = video_upload.objects.filter(draft=False).exclude(id=id)
    v=get_object_or_404(video_upload,pk=id)
    user = get_object_or_404(User, id=request.user.id)

    user_p = author.objects.filter(author_name=user.id)
    if user_p:
        u = get_object_or_404(author, author_name=user.id)
        context = {
            "video": all_video,
            "vid": v,
            "user_profile": u,
        }
        return render(request, 'play_draft.html', context)
    else:
        name = get_object_or_404(User, id=request.user.id)
        f_name = name.first_name
        first_latter = f_name[0]

        context = {
            "video": all_video,
            "first_letter": first_latter,

        }
        return render(request, 'play_draft.html', context)


def published_video(request,id):
    pub_video=get_object_or_404(video_upload,pk=id)
    pub_video.draft=True
    pub_video.save()

    return redirect('home')

def video_home(request):
    if request.user.is_authenticated:

        tutorial=video_upload.objects.filter(draft=True,category__name="Tutorial")
        natok = video_upload.objects.filter(draft=True, category__name="Natok")
        song = video_upload.objects.filter(draft=True, category__name="Song")
        movie = video_upload.objects.filter(draft=True, category__name="Movie")
        funny_video = video_upload.objects.filter(draft=True, category__name="Funny Video")
        latest_song = video_upload.objects.filter(draft=True, category__name="Latest Song")


        user = get_object_or_404(User, id=request.user.id)

        user_p = author.objects.filter(author_name=user.id)
        if user_p:
            u = get_object_or_404(author, author_name=user.id)

            context = {

                "user_profile": u,
                "tutorial":tutorial,
                "natok":natok,
                "song":song,
                "movie": movie,
                "funny_video": funny_video,
                "latest_song": latest_song,

            }
            return render(request, 'home.html', context)
        else:
            name = get_object_or_404(User, id=request.user.id)
            f_name = name.first_name
            first_latter = f_name[0]

            context = {
                "tutorial": tutorial,
                "natok": natok,
                "song": song,
                "movie":movie,
                "funny_video":funny_video,
                "latest_song":latest_song,
                "first_letter": first_latter,

            }
            return render(request, 'home.html', context)




    else:
        return redirect('sign-in')


def play_video(request, id):
    v = get_object_or_404(video_upload, pk=id)
    t_v = video_upload.objects.filter(draft=True).exclude(id=id)
    getcomment = comment.objects.filter(post=id).order_by('-id')
    all = comment.objects.filter(post=id).count()

    user = get_object_or_404(User, id=request.user.id)

    check_id = history.objects.filter(v_id=id,name=user)
    if check_id:
        history.objects.filter(v_id=id,name=user).delete()
        H_obj = history.objects.create(name=user, v_id=id)
        H_obj.save()

    else:
        H_obj = history.objects.create(name=user, v_id=id)
        H_obj.save()

    is_liked = False
    if v.likes.filter(id=request.user.id).exists():
        is_liked = True

    form = commentForm(request.POST or None)
    if request.is_ajax():
        form = commentForm(request.POST or None)
        if form.is_valid():
            u = get_object_or_404(author, author_name=request.user.id)
            instance = form.save(commit=False)
            instance.post = v
            instance.commented_name = u
            instance.save()

            data = {
                'message': 'form is save'
            }
            return JsonResponse(data)

    all_ip = user_ip.objects.filter(video=id).count()
    ip = request.META.get('REMOTE_ADDR')
    client_ip = user_ip.objects.filter(ip=ip, video=id)
    if client_ip:
        pass
    else:
        user_ip.objects.create(ip=ip, video=v)

    li = []
    for x in t_v:
        li.append(x)

    random.shuffle(li)
    user = get_object_or_404(User, id=request.user.id)
    user_p = author.objects.filter(author_name=user.id)
    if user_p:
        u = get_object_or_404(author, author_name=user.id)
        context = {
            "vid": v,
            "more": li,
            "comment": getcomment,
            "form": form,
            "all_comment": all,
            "is_liked": is_liked,
            "total_likes": v.total_likes(),
            "views": all_ip,
            "user_profile": u,
        }
        return render(request, 'play_video.html', context)
    else:
        name = get_object_or_404(User, id=request.user.id)
        f_name = name.first_name
        first_latter = f_name[0]

        context = {
            "vid": v,
            "more": li,
            "comment": getcomment,
            "form": form,
            "all_comment": all,
            "is_liked": is_liked,
            "total_likes": v.total_likes(),
            "views": all_ip,

            "first_letter": first_latter,
        }
        return render(request, 'play_video.html', context)


def like_video(request):
    # like section
    if request.user.is_authenticated:
        video = get_object_or_404(video_upload, id=request.POST.get('video_id'))
        is_liked = False
        if video.likes.filter(id=request.user.id).exists():
            video.likes.remove(request.user)
            is_liked = False
        else:
            video.likes.add(request.user)
            is_liked = True
        return redirect('show', id=video.id)
    else:
        return redirect('sign-in')


def upload_video_file(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        user_p = author.objects.filter(author_name=user.id)
        if user_p:
            u = get_object_or_404(author, author_name=user.id)
            form = U_video(request.POST or None, request.FILES or None)
            if form.is_valid():
                u = get_object_or_404(author, author_name=user.id)
                instance = form.save(commit=False)
                instance.uploader_name = u
                instance.save()
                return redirect('home')
            return render(request, 'upload_video.html', {"form": form, "user_profile": u, })

        else:
            return redirect('create_channel')


    else:
        return redirect('signup')


def search(request):
    if request.method == "POST":
        srch = request.POST['srch']

        if srch:
            match = video_upload.objects.filter(Q(video_title__icontains=srch))

            if match:
                user = get_object_or_404(User, id=request.user.id)
                user_p = author.objects.filter(author_name=user.id)
                if user_p:
                    u = get_object_or_404(author, author_name=user.id)
                    context = {
                        "video_found": match,
                        "user_profile": u,

                    }
                    return render(request, 'search.html', context)
                else:
                    name = get_object_or_404(User, id=request.user.id)
                    f_name = name.first_name
                    first_latter = f_name[0]
                    context = {
                        "video_found": match,
                        "first_letter": first_latter,

                    }
                    return render(request, 'search.html', context)
            else:
                messages.error(request, 'no result found')
        else:
            return HttpResponseRedirect('/search/')
    return render(request, 'search.html')



def video_history(request):


    user = get_object_or_404(User, id=request.user.id)
    user_p = author.objects.filter(author_name=user.id)
    all_video=history.objects.filter(name=user).order_by('-id')
    li=[]
    for a in all_video:
        k=video_upload.objects.filter(id=a.v_id)

        li.append(k)

    li=list(itertools.chain(*li))
    if user_p:
        u = get_object_or_404(author, author_name=user.id)
        context = {

            "user_profile": u,
            "video":li,
            "user":user,


        }
        return render(request, 'history.html', context)
    else:
        name = get_object_or_404(User, id=request.user.id)
        f_name = name.first_name
        first_latter = f_name[0]
        context = {

            "first_letter": first_latter,
            "video":li,
            "user":user,


        }
        return render(request, 'history.html', context)


def watch_l(request,id):
    user = get_object_or_404(User, id=request.user.id)

    check_id = watch_later.objects.filter(v_id=id,name=user)
    if check_id:
        watch_later.objects.filter(v_id=id,name=user).delete()
        H_obj = watch_later.objects.create(name=user, v_id=id)
        H_obj.save()

    else:
        H_obj = watch_later.objects.create(name=user, v_id=id)
        H_obj.save()

    return redirect('show_watch')



def show_watch_later(request):
    user=get_object_or_404(User,id=request.user.id)

    all_watch=watch_later.objects.filter(name=user).order_by('-id')
    count_video=watch_later.objects.filter(name=user).count()

    li = []
    for a in all_watch:
        k = video_upload.objects.filter(id=a.v_id)

        li.append(k)

    li = list(itertools.chain(*li))
    user_p = author.objects.filter(author_name=user.id)
    if user_p:
        u = get_object_or_404(author, author_name=user.id)
        context = {
            "w_video": li,
            "video": count_video,
            "user_profile": u,
        }

        return render(request, 'watch.html', context)
    else:

        f_name = user.first_name
        first_latter = f_name[0]
        context = {

            "first_letter": first_latter,
            "w_video": li,
            "video": count_video,


        }
        return render(request, 'watch.html', context)









def clear_history(request):
    user = get_object_or_404(User, id=request.user.id)
    history.objects.filter(name=user).delete()

    return redirect('history')

def delete_draft(request,id):
    get_video = video_upload.objects.get(id=id)
    video_upload.objects.get(id=id).delete()

    uploader_email=get_video.uploader_name.author_name.email
    uploader_first_name=get_video.uploader_name.author_name.first_name
    uploader_last_name = get_video.uploader_name.author_name.last_name
    title=get_video.video_title

    subject="Rejected your uploading video"
    body="Hi"+"\t" + uploader_first_name + uploader_last_name +"\n" + title + "\n" + "your uploading video Rejected on mytube Administrator"

    send_mail(subject, body, 'imranhossainrsi2015@gmail.com', [uploader_email], fail_silently=False, )

    return redirect('draft')







def clear_watch(request):
    user = get_object_or_404(User, id=request.user.id)
    watch_later.objects.filter(name=user).delete()
    return redirect('show_watch')

def delete_watch(request,id):
    user=get_object_or_404(User,id=request.user.id)
    watch_later.objects.filter(name=user,v_id=id).delete()
    return redirect('show_watch')





