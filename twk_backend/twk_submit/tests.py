from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

from twk_auth.views import login

from twk_load.views import load_hw

from twk_save.views import save_publish_hw

from .views import submit_hw, get_code

import json, base64, os

from twk_send.views import peer_review_task_dispatch

from twk_auth.views import isLogined

"""
this test should open judge 0 server and set environment variable first, or it would be failed
"""
class twk_submit_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username='test', password='password',email='james@yahoo.com.tw')
        self.user2 = User.objects.create(
            username='test2', password='password', email='jjanes@yahoo.com.tw'
        )

    def test_details(self):
        self.submit_hw(self.user) #submit a hw by user1
        self.get_code(self.user, 1) #load submit by id = 1 

        self.islogin(self.user)
        self.islogin(self.user2)
        
        response = self.send_peer_review(self.user)
        self.assertEqual(response.status_code, 409)

        self.submit_hw(self.user2)
        response = self.send_peer_review(self.user)
        self.assertEqual(response.status_code, 200)

    def submit_hw(self, username):
        publish_data = { "question": "question1", "stdin": "1 1", "stdout":"2", "language_id":"4" }
        request = self.factory.post('/publish_hw/', json.dumps(publish_data), content_type='application/json')

        request.user = username
        save_publish_hw(request)
        s = base64.b64encode(b'int main () { printf("2"); return 0; }')
        s = s.decode("utf-8")

        submit_data = { 'source_code': s , "language_id": "4", "assignment_id": "1"}
        request = self.factory.post('/submit_hw/', submit_data, Accept='application/json')
        request.user = username
        response = submit_hw(request)

        self.assertEqual(response.status_code, 200)

        request.user = AnonymousUser()
        response = submit_hw(request)

        self.assertEqual(response.status_code, 302)

    def get_code(self, username, count):
        request = self.factory.get('/get_code/1/')
        request.user = username
        response = get_code(request, count)

        self.assertEqual(response.status_code, 200)

    def send_peer_review(self, username):
        request = self.factory.get('/peer_review_task_dispatch')
        request = username
        return peer_review_task_dispatch(request)

    def islogin(self, username):
        request = self.factory.get('/isLogined/')
        request.user = username
        response = isLogined(request)
    
    


        

        