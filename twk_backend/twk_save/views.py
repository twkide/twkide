from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core import serializers

import json

from twk_save.models import SavedHW, PublishHW

# TODO: Make sure user don't loss their code if theire session timed out for some reason
@login_required(login_url='/login/') # https://docs.djangoproject.com/en/2.0/topics/auth/default/#the-login-required-decorator
def save_hw(request):
    if request.user.is_authenticated:
        if(request.POST):
            u = SavedHW.objects.filter(user=request.user,file_name=request.POST['filename']).delete()
            d = json.loads(request.POST['content'])
            p = SavedHW.objects.create( source_code = d['source_code'],
                                        stdin = d['stdin'],
                                        language_id = d['language_id'],
                                        file_name = request.POST['filename'],
                                        user = request.user
                                      )
            p.save()
            print("homework saved. user = " + str(request.user))
        return JsonResponse({'a':'a'})
    print("unauthorized user tries to save hw")
    return HttpResponse('Unauthorized', status=401)

# @login_required(login_url='/login/')
def save_publish_hw(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        p = PublishHW.objects.create(question = data['question'], stdin = data['stdin'],
                                     stdout = data['stdout'], language_id = data['language_id'])
        p.save()
        
        return HttpResponse('success', 200)
    elif request.method == 'GET':
        p = PublishHW.objects.all()
        data = serializers.serialize('json', p)
        struct = json.loads(data)
        return JsonResponse(struct, safe=False)

# @login_required(login_url='/login/') # https://docs.djangoproject.com/en/2.0/topics/auth/default/#the-login-required-decorator
def load_publish_hw(request, id):
    if request.method == 'GET':
        p = PublishHW.objects.get(id = id)
        
        res = {
            'id' : p.id,
            'question': p.question,
            'stdin': p.stdin,
            'stdout': p.stdout,
            'language_id': p.language_id
        }
        
        return JsonResponse(res)
    return HttpResponse('Unauthorized', 401)
