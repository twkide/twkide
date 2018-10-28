
from django.db import models
from django.contrib.auth.models import User

class RocketChatPass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='have_chat_password')
    pw = models.TextField()
    def __str__(self):
        return str(self.user)
