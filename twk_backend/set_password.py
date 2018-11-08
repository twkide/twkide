
from django.contrib.auth.models import User

for user in User.objects.all():
    user.set_password(user.password)
    user.save()

user = User.objects.create(username='admin', password='password')
user.set_password(user.password)
user.is_superuser=True
user.is_staff=True
user.save()

