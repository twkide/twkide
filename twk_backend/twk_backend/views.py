from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
import twk_send.views as send
import os
from twk_save.models import PublishHW
def homepage(request):
    # TODO: homepage
    return HttpResponse('<h1>This is homepage.</h1>')

def js_ide_js(request):
    return render(request, 'js/ide.js', {
        'judge0_api_url': os.environ["JUDGE0_API_PUBLIC_URL"],
        'twk_url': os.environ["TWK_URL"]
    })

def ide_html(request):
    username = "User"
    publish_hws = PublishHW.objects.all()
    add_new = ""
    peer_review = ""
    if request.user.is_staff:
        add_new='<a href="{}/templates/upload.html">Add new Assignment</a>'.format(os.environ["TWK_URL"])
        peer_review='<a href="{}/peer_review_task_dispatch">Send peer review instructions to students</a>'.format(os.environ["TWK_URL"])
    if request.user.is_authenticated:
        username = request.user.get_username()
    count = send.get_unread_message(request.user)
    return render(request, 'ide.html', {
       'add_new':add_new,
       'peer_review':peer_review,
       'rocket_chat_url': os.environ["ROCKET_CHAT_PUBLIC_URL"],
       'User':username,
       'publish_hws':publish_hws,
       'count': count
    })

def upload_html(request):
    username = "User"
    if request.user.is_authenticated:
        username = request.user.get_username()
    return render(request, 'upload.html', {
    })

def user_html(request):
    return render(request, 'user_page.html', {
        'twk_url': os.environ["TWK_URL"]
    })

