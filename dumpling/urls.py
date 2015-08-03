from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'css/(?P<name>.*)\.css$', views.styles, name='styles'),
    url(r'(?P<path>.*)', views.PageView.as_view()),
]
