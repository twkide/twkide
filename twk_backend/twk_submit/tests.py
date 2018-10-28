from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase, Client

from twk_auth.views import login

from twk_load.views import load_hw

import json

class twk_submit_test(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username='test', password='password')

    def test_details(self):
        # Create an instance of a GET request.
        c = Client()
        data = { 'question': 'question1', 'stdin': '1 1', 'stdout':'2', 'language_id':'4'}
        response = self.client.post('/publish_hw/', data = json.dumps(data), content_type='application/json')

        data = {'source_code':'printf("Hello World!")', 'language_id': '4', 'assignment_id': '1'}
        request = self.factory.post('/load_hw/', data, format = 'json')

        request.user = self.user

        
        # Test my_view() as if it were deployed at /customer/details
        print("12313132")
        print(request)
        print("1231313")
        
        # Use this syntax for class-based views.
        # response = MyView.as_view()(request)
        # self.assertEqual(response.status_code, 200)