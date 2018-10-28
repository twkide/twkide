from django.contrib import admin

# Register your models here.
from .models import SubmitHW, ReviseHW

admin.site.register(SubmitHW)

admin.site.register(ReviseHW)
