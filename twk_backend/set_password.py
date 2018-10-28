
from django.contrib.auth.models import User

for user in User.objects.all():
    user.set_password(user.password)
    user.save()

