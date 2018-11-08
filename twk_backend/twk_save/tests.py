from django.test import TestCase, RequestFactory

from .views import save_publish_hw, load_publish_hw
from django.contrib.auth.models import User

import json

class twk_submit_test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username='test', password='password',email='james@yahoo.com.tw')

    def test_details(self):
        publish_data = { "question": "question1", "stdin": "1 1", "stdout":"2", "language_id":"4" }
        request = self.factory.post('/publish_hw/', json.dumps(publish_data), content_type='application/json')

        request.user = self.user
        save_publish_hw(request)

        request = self.factory.get('/publish_hw/1/')
        request.user = self.user
        response = load_publish_hw(request, 1)

        self.assertEqual(response.status_code, 200)

        request = self.factory.get('publish_hw/')
        request.user = self.user
        response = save_publish_hw(request)
        
        self.assertEqual(response.status_code, 200)
        