
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^templates/$', views.TemplateList.as_view()),
    url(r'^media/$', views.MediaList.as_view()),
]
