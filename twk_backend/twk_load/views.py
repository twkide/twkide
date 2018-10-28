from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt

import json

from twk_save.models import SavedHW

@login_required(login_url='/login/')
def load_hw(request):
    if request.user.is_authenticated:
        if request.POST:
            u = SavedHW.objects.get(user=request.user,file_name=request.POST['filename'])
            print(request.user)
    return JsonResponse({'source_code':u.source_code,'stdin':u.stdin,'language_id':u.language_id})
