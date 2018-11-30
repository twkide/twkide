
import twk_auth.views as auth

from twk_submit.models import SubmitHW

from django.http import HttpResponse
import requests
import os
import json
from django.contrib.auth.models import User
import random
from django.template import Template, Context

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
    t =Template("""
            <style>
                
.button {
  border-radius: 4px;
  background-color: #f4511e;
  border: none;
  color: #FFFFFF;
  text-align: center;
  font-size: 20px;
  padding: 20px;
  width: 150px;
  transition: all 0.5s;
  cursor: pointer;
  margin: 5px;
}

.button span {
  cursor: pointer;
  display: inline-block;
  position: relative;
  transition: 0.5s;
}

.button span:after {
  content: '<';
  position: absolute;
  opacity: 0;
  top: 0;
  left: -20px;
  transition: 0.5s;
}

.button:hover span {
  padding-left: 25px;
}

.button:hover span:after {
  opacity: 1;
  left: 0;
}
div {
    font-family:"Arial Black";
    font-size:20px;
}
            </style>
            <button class="button" onclick=func()><span>Back</span></button>
            <div>{{text}}</div>
            <script>
            function func() {
                window.location.replace("{{twk_url}}/templates/ide.html");
            }
            </script>
        """)
    """
    if request.user.is_staff == False:
        c = Context({"text": "Permission denied","twk_url":os.environ["TWK_URL"]})
        return HttpResponse(t.render(c), status = 409)
    """
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
            c = Context({"text": "Replicated submissions from same user","twk_url":os.environ["TWK_URL"]})
            return HttpResponse(t.render(c), status = 409)
        visited[hw.user_id] = True
    if len(user_ids) <= 1:
        c = Context({"text": 'No enough submissions to dispatch',"twk_url":os.environ["TWK_URL"]})
        return HttpResponse(t.render(c), status = 409)
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
    c = Context({"text": 'Success',"twk_url":os.environ["TWK_URL"]})
    return HttpResponse(t.render(c), status = 200)

def rocket_chat_send_im(user, msg, headers):
    print("sending messge \"", msg, "\" to user ", user)
    r = requests.post(os.environ["ROCKET_CHAT_PRIVATE_URL"] +
                      "/api/v1/im.create", headers = headers, json = {'username': user} )
    assert r.status_code == 200
    r = requests.post(os.environ["ROCKET_CHAT_PRIVATE_URL"] +
                      "/api/v1/chat.postMessage", headers = headers, json = {'roomId': r.json()['room']['_id'], 'text': msg})
    assert r.status_code == 200

