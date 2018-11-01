from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase, Client

from twk_auth.views import login

from twk_load.views import load_hw

from twk_save.views import save_publish_hw

from .views import submit_hw, get_code

import json, base64

"""
this test should open judge 0 server and set environment variable first, or it would be failed
"""
class twk_submit_test(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username='test', password='password',email='james@yahoo.com.tw')

    def test_details(self):
        publish_data = { "question": "question1", "stdin": "1 1", "stdout":"2", "language_id":"4" }
        request = self.factory.post('/publish_hw/', json.dumps(publish_data), content_type='application/json')

        save_publish_hw(request)
        s = base64.b64encode(bytes('your string', 'utf-8'))
        print(s)
        submit_data = { 'source_code': s , "language_id": "4", "assignment_id": "1"}
        request = self.factory.post('/submit_hw/', submit_data, Accept='application/json')
        request.user = self.user
        response = submit_hw(request)

        self.assertEqual(response.status_code, 200)

        request.user = AnonymousUser()
        response = submit_hw(request)

        self.assertEqual(response.status_code, 302)

        request = self.factory.get('/get_code/1/')
        request.user = self.user
        response = get_code(request, 1)

        print(response)
        self.assertEqual(response.status_code, 200)
        

