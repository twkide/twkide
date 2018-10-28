"""twk_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.conf.urls import include

import twk_auth.views
import twk_save.views
import twk_backend.views
import twk_load.views
import twk_submit.views
import twk_send.views

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', RedirectView.as_view(url = '/login/')),
    url(r'^login$', RedirectView.as_view(url = '/login/')),
    url(r'^login/$', twk_auth.views.login),
    url(r'^save_hw$', RedirectView.as_view(url = '/save_hw/')),
    url(r'^save_hw/?$', twk_save.views.save_hw),
    url(r'^load_hw$', RedirectView.as_view(url = '/load_hw/')),
    url(r'^load_hw/?$', twk_load.views.load_hw),
    url(r'^submit_hw$', RedirectView.as_view(url = '/submit_hw/')),
    url(r'^submit_hw/?$', twk_submit.views.submit_hw),
    url(r'^revise_hw$', RedirectView.as_view(url = '/revise_hw/')),
    url(r'^revise_hw/?$', twk_submit.views.revise_hw),
    url(r'^view_peer_review_results$', RedirectView.as_view(url = '/view_peer_review_results/')),
    url(r'^view_peer_review_results/?$', twk_submit.views.view_peer_review_results),
    url(r'get_code/(?P<id>[-\w]+)/', twk_submit.views.get_code),
    url(r'^publish_hw/(?P<id>[-\w]+)/', twk_save.views.load_publish_hw),
    url(r'^publish_hw/', twk_save.views.save_publish_hw),
    url(r'^send_msg$', RedirectView.as_view(url='/send_msg/')),
    url(r'^send_msg/?$', twk_send.views.send_message),
    url(r'^peer_review_task_dispatch$', RedirectView.as_view(url='/peer_review_task_dispatch/')),
    url(r'^peer_review_task_dispatch/?$', twk_send.views.peer_review_task_dispatch),
    url(r'^isLogined$', RedirectView.as_view(url = '/isLogined/')),
    url(r'^isLogined/$', twk_auth.views.isLogined),
    url(r'^logout/$', twk_auth.views.logout),
    url('admin/', admin.site.urls),
    url(r'^templates/js/ide.js$', twk_backend.views.js_ide_js),
    url(r'^templates/ide.html$', twk_backend.views.ide_html),
    url(r'^templates/upload.html$', twk_backend.views.upload_html),
    url(r'^templates/user$', twk_backend.views.user_html),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

