from django.test import TestCase, RequestFactory
from twk_auth.views import login
from django.contrib.auth.models import User

class Login(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username='test', password='password')

    def test_details(self):
        # Create an instance of a GET request.
        user = self.user
        request = self.factory.post('/login/', {"username":"test","password":"password"})
        
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        # request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        print(request)
        # Use this syntax for class-based views.
        # response = MyView.as_view()(request)
        # self.assertEqual(response.status_code, 200)
        
