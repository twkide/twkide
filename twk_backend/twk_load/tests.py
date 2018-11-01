from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase, Client

from twk_auth.views import login

from twk_load.views import load_hw

from twk_save.views import save_hw

import json

class twk_submit_test(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username='test', password='password')

    def test_details(self):
        #save_hw post data
        content = {'stdin': '1 1', 'source_code':'print("1")', 'language_id':'4'}
        data = { 'content': json.dumps(content), 'filename': 'test'}

        #mock login to save hw
        request = self.factory.post('/save_hw/', data, format = 'json')
        request.user = self.user
        save_hw(request)

        #load_hw post data
        data = {'source_code':'printf("Hello World!")', 'language_id': '4', 'assignment_id': '1', 'filename': 'test'}
        request = self.factory.post('/load_hw/', data, format = 'json')

        request.user = self.user # login
        response = load_hw(request)
        self.assertEqual(response.status_code, 200)

        request.user = AnonymousUser()#not login
        response = load_hw(request)
        self.assertEqual(response.status_code, 302)