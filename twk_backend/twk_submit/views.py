from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework.response import Response
import requests
from requests import Session
import json
import os
import time
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import base64
from datetime import datetime
from twk_submit.models import SubmitHW
from twk_submit.models import ReviseHW
from twk_save.models import PublishHW
from django.template import Template, Context

@login_required(login_url='/login/')
def submit_hw(request):
    if request.user.is_authenticated:
        if request.POST:
            print(request.POST)
            print(request.POST['source_code'])
            print(request.POST['language_id'])
            print(request.POST['assignment_id'])

            try:
                my_submit = SubmitHW.objects.get(user_id = request.user)
                my_submit.time = datetime.now()
                my_submit.language_id = request.POST['language_id']
                my_submit.source_code = request.POST['source_code']
                my_submit.hw_id = PublishHW.objects.get(id = request.POST['assignment_id'])
            except:
                my_submit = SubmitHW.objects.create(
                                user_id = request.user, time = datetime.now(),
                                source_code = request.POST['source_code'],
                                language_id = request.POST['language_id'],
                                hw_id = PublishHW.objects.get(id = request.POST['assignment_id'])
                            )
                my_submit.save()
            #d = json.loads(request.POST['content'])
            payload={'source_code':request.POST['source_code'],
                    'language_id':request.POST['language_id'],
                    'stdin':base64.b64encode(b'1 1'),
                    'expected_output': base64.b64encode(b'2'),
                    }
            headers={
                'async': "True",
                'contentType': "application/json",
            }
            r=requests.post(os.environ["JUDGE0_API_PRIVATE_URL"] + "/submissions?base64_encoded=true&wait=true",data=payload,headers=headers)
            print(r.json())
            isAC = "Accepted" in (r.json()['status'])['description']
            if isAC :
                try:
                    my_submit = SubmitHW.objects.get(user_id = request.user)
                    my_submit.time = datetime.now();
                    my_submit.source_code = request.POST['source_code']
                    my_submit.save()
                except:
                    my_submit = SubmitHW.objects.create(user_id = request.user, time = datetime.now(), source_code = request.POST['source_code'])
                    my_submit.save();
            payloads = { 'id': (r.json()['status'])["id"],
                         'description': ((r.json()['status'])['description'] + " (" + ("" if isAC else "not ") + "ready for peer review).")
                       }
            return JsonResponse(payloads)
    return HttpResponse('Unauthorized', 401)

@login_required(login_url='/login/')
def get_code(request, id):
    # TODO: check if user is authorized to get code!
    print(id)
    print(request.method)
    if request.method == 'GET':
        print("123112313")
        homework = SubmitHW.objects.get(id = id)
        payloads={'user_id': homework.user_id.id,
                  'source_code': homework.source_code, 'time': homework.time, 'language_id': homework.language_id}
        return JsonResponse(payloads)
    return HttpResponse('success', 200)

@login_required(login_url='/login/')
def revise_hw(request):
    # TODO: check if user is authorized to revise the hw!
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        hw_id = SubmitHW.objects.get(id = data['id'])
        print(request.user)
        ReviseHW.objects.create(
            reviewee = hw_id.user_id,
            hw_id = hw_id,
            time = datetime.now(),
            console = data['console'],
            reviewer = request.user,
            error_text = data['error_text']
        ).save()
        revise.save()
        return HttpResponse('success', 200)
    return HttpResponse('Unauthorized method', 401)

@login_required(login_url='/login/')
def view_peer_review_results(request):
    # TODO: check if user is permissioned to view this!
    t = Template("""
            <style>
                table {
                    border-collapse: collapse;
                    width: 100%;
                }

                th, td {
                    padding: 8px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
            </style>
            <div id="table">
            <table border=1>
            <thead>
                <tr>
                    <th>problem id</th>
                    <th>reviewee</th>
                    <th>reviewer</th>
                    <th>comment</th>
                </tr>
            </thead>
            <tbody>
                {% for rev in reviews %}
                    <tr>
                    {% for attr in rev %}
                        <td>{{ attr }}</td>
                    {% endfor %}
                    </tr>
                {% endfor %}
            </tbody>
            </table>
            </div>
        """)
    vals = []
    if request.user.is_superuser:
        rhws = ReviseHW.objects.all()
    else:
        rhws = ReviseHW.objects.filter(reviewee = request.user)
    for rhw in rhws:
        tmp = [str(rhw.hw_id.hw_id), str(rhw.reviewee), str(rhw.reviewer), str(rhw.error_text)]
        vals.append(tmp)
    c = Context({"reviews": vals})
    return HttpResponse(t.render(c))