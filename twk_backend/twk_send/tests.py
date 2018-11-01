from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase, Client

from twk_auth.views import login

from twk_load.views import load_hw

from twk_save.views import save_hw

