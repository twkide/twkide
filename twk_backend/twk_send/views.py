
import twk_auth.views as auth

from twk_submit.models import SubmitHW

from django.http import HttpResponse
import requests
import os
import json
from django.contrib.auth.models import User
import random

def get_headers():
    userId, token = auth.getAdminAuthToken();
    return {'X-Auth-Token': token, 'X-User-Id': userId, 'content-type': 'application/json' }

def send_message(request):
    if request.method == 'POST':
        j = json.loads(request.body)
        rocket_chat_send_im(j['user'], j['msg'], get_headers())
        return HttpResponse('success', 200)
    return HttpResponse('You should use POST', status=401)

def peer_review_task_dispatch(request):
    if not request.user.is_staff:
        return HttpResponse('permission denied', status = 409)
    hws = SubmitHW.objects.all()
    print("hwshwshwshwshws")
    for i in hws:
        print(i)
    user_ids = []
    hw_ids = []
    visited = {}
    for hw in SubmitHW.objects.all():
        hw_ids.append(hw.id)
        user_ids.append(hw.user_id)
        if hw.user_id in visited:
            return HttpResponse('replicated submissions from same user', status = 409)
        visited[hw.user_id] = True
    if len(user_ids) <= 1:
        return HttpResponse('no enough submissions to dispatch', status = 409)
    assigned_hw_id = {}
    print("hw_ids = ", hw_ids)
    print("user_ids = ", user_ids)
    for i in range(0, len(hw_ids)):
        uid_idx = 0
        while (user_ids[uid_idx] in assigned_hw_id) or uid_idx == i:
            uid_idx = random.randint(0, len(hw_ids)-1)
        assigned_hw_id[user_ids[uid_idx]] = hw_ids[i]
        msg = 'Your classmates have some homeworks waiting your review!\n' + os.environ["TWK_URL"] + "#" + str(hw_ids[i])
        rocket_chat_send_im(str(user_ids[uid_idx]), msg, get_headers())
    return HttpResponse('success', status = 200)

def rocket_chat_send_im(user, msg, headers):
    print("sending messge \"", msg, "\" to user ", user)
    r = requests.post(os.environ["ROCKET_CHAT_PRIVATE_URL"] +
                      "/api/v1/im.create", headers = headers, json = {'username': user} )
    assert r.status_code == 200
    r = requests.post(os.environ["ROCKET_CHAT_PRIVATE_URL"] +
                      "/api/v1/chat.postMessage", headers = headers, json = {'roomId': r.json()['room']['_id'], 'text': msg})
    assert r.status_code == 200

