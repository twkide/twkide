from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
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
    if request.user.is_authenticated:
        username = request.user.get_username()
    return render(request, 'ide.html', {
       'rocket_chat_url': os.environ["ROCKET_CHAT_PUBLIC_URL"],
       'User':username,
       'publish_hws':publish_hws
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

