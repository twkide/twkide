from django.test import TestCase, Client

from twk_save.models import PublishHW
import json
from rest_framework.test import APITestCase


# Create your tests here.
# 
class PublishHWTestCase(APITestCase):
    def test_get_PublishHW(self):
        data = { 'question': 'question1', 'stdin': "1 1", 'stdout':'2', 'language_id':'4'}
       
        response = self.client.post('/publish_hw/', data, format='json')

        response = self.client.get('/publish_hw/1/')
        test_data = json.loads(response.content)
        self.assertEqual(test_data['id'], 1)
        self.assertEqual(test_data['question'], data['question'])
        self.assertEqual(test_data['stdin'], data['stdin'])
        self.assertEqual(test_data['stdout'], data['stdout'])
        self.assertEqual(test_data['language_id'], data['language_id'])

        response = self.client.get('/publish_hw/')

        self.assertEqual(response.status_code, 200)