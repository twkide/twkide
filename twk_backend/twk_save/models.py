from django.db import models
from django.contrib.auth.models import User

class SavedHW(models.Model):
    source_code = models.TextField()
    stdin = models.TextField()
    language_id = models.TextField()
    file_name = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user) + "'s hw" + str(self.file_name) 

class PublishHW(models.Model):
    question = models.TextField()
    stdin = models.TextField()
    stdout = models.TextField()
    language_id = models.TextField()
