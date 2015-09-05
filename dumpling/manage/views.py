import os

from django.conf import settings
from django.shortcuts import render
from django.utils._os import safe_join

from nap.rest import views

from . import mappers
from ..models import Page


def index(request):
    return render(request, 'dumpling/index.html', {
        'roots': Page.objects.filter(parent=None),
    })


class TemplateList(views.BaseListView):
    mapper_class = mappers.PageMapper

    def get(self, request, *args, **kwargs):
        root = kwargs.get('root', '')
        base_path = safe_join(settings.USER_TEMPLATES_PATH, root)

        return self.multiple_response(object_list=[
            (fn, os.stat(os.path.join(base_path, fn)))
            for fn in os.listdir(base_path)
            if not fn.startswith('.')
        ])
