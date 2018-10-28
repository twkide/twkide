from django.shortcuts import render
from django.contrib import auth, messages
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt

import requests
import json
import string
import random
import os

from twk_auth.models import RocketChatPass

# https://stackoverflow.com/questions/33267383/how-to-configure-x-frame-options-in-django-to-allow-iframe-embedding-of-one-view
# to allow rocket chat load login page as iframe
@xframe_options_exempt
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(os.environ["TWK_URL"]+"/templates/ide.html")
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
    except:
        user = None
    if user is not None:
        if user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect('/templates/ide.html')
    else:
        if request.POST:
            messages.error(request,'帳號或密碼錯誤!!')
        return render(request,'login.html')
    return render(request,'login.html')

# TODO: move these rocket chat functions to another place
def getAuthToken(username, password):
    # https://rocket.chat/docs/developer-guides/rest-api/authentication/login/
    payload = { 'username': username, 'password': password }
    print("try to login user " + username)
    r = requests.post(os.environ["ROCKET_CHAT_PRIVATE_URL"] + "/api/v1/login", json = payload)
    print(r.json())
    if r.status_code == requests.codes.ok:
        d = r.json()['data']
        return d['userId'], d['authToken']
    else:
        return None, None

def getAdminAuthToken():
    return getAuthToken(os.environ['ROCKET_CHAT_ADMIN_ACCOUNT'], os.environ['ROCKET_CHAT_ADMIN_PASSWORD'])

def registerRocketUser(username, password):
    adminUid, adminAuthToken = getAdminAuthToken() # TODO: We should reuse admin auth token rather than create a new one
    if adminAuthToken == None:
        print("Rocket chat admin failed to log in")
        return False
    payload = { 'name': username, 'email': (username+"@twkide.org"), 'username': username, 'password': password }
    headers = { 'X-Auth-Token': adminAuthToken, 'X-User-Id': adminUid }
    print("creating user...")
    r = requests.post(os.environ["ROCKET_CHAT_PRIVATE_URL"] + "/api/v1/users.create", headers = headers, json = payload)
    print(r.json())
    if r.status_code == requests.codes.ok:
        return True
    else:
        print("rocket chat server returned status code " + str(r.status_code) + " when creating user")
        return False

def isLogined(request):
    if request.user.is_authenticated:
        # step 1. Query user's corresponding rocket chat account's password, if user's rocket account not found in db,
        #         create one for him/her then store his/her rocket chat password in db.
        # step 2. use rocket chat's login API to get user's `authToken`. https://rocket.chat/docs/developer-guides/rest-api/authentication/login/
        # step 3. return the auth token
        rcp = RocketChatPass.objects.filter(user = request.user)
        if rcp:
            _, t = getAuthToken(str(request.user), str(rcp[0].pw))
            return JsonResponse({'token': t, 'loginToken': t})
        else:
            # print("rocket chat password of " + request.user + " not found. Trying to create an account for him.")
            print("rocket chat password not found for user " + str(request.user))
            # TODO: password security concern
            pw = ''.join(random.choices( string.ascii_uppercase +
                                         string.ascii_lowercase +
                                         string.digits,
                                         k=16)) # TODO: turn this code into a reusable function
            if registerRocketUser(str(request.user), pw):
                obj = RocketChatPass.objects.create(user = request.user, pw = pw)
                obj.save()
                return isLogined(request) # Let's hope this won't cause infinite recursion
            else:
                # Hmm... something goes wrong
                print("Cannot successfully register user for Rocket chat")
                return HttpResponse('Unauthorized', status=401)
    else:
        return HttpResponse('Unauthorized', status=401)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(os.environ["TWK_URL"]+"/login/")
