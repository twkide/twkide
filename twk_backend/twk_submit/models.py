from django.db import models
from django.contrib.auth.models import User
from twk_save.models import PublishHW  
class SubmitHW(models.Model):
     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
     hw_id = models.ForeignKey(PublishHW, on_delete=models.CASCADE)
     source_code = models.TextField()
     time = models.DateTimeField()
     language_id = models.TextField(default="")
     def __str__(self):
         return str(self.user_id)

class ReviseHW(models.Model):
    hw_id = models.ForeignKey(SubmitHW, on_delete=models.CASCADE) # Do we really want cascade?
    # TODO: clean up schema, it is better to have separate model for "is reviewed by" relationship
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewee')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer')
    time = models.DateTimeField()
    console = models.BooleanField()
    error_text = models.TextField(blank = True)

