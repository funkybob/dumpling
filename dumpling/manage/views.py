import os
import mimetypes

from django.conf import settings
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.utils._os import safe_join

from nap.rest import views

from ..models import Page
from ..utils import json


def index(request):
    return render(request, 'dumpling/index.html', {
        'roots': Page.objects.filter(parent=None),
    })


class TemplateList(views.BaseListView):

    def get(self, request, *args, **kwargs):
        root = kwargs.get('root', '')
        base_path = safe_join(settings.USER_TEMPLATES_PATH, root)

        return StreamingHttpResponse(
            json.dumps(dir_meta(base_path)),
            content_type='application/json',
        )


class MediaList(views.BaseListView):

    def get(self, request, *args, **kwargs):

        return StreamingHttpResponse(
            json.dumps(dir_meta(settings.MEDIA_ROOT)),
            content_type='application/json',
        )


def dir_meta(path):
    '''
        {
            name: filename,
            path: path/from/root/filename
            content_type: 'image/jpeg',
            size: in_bytes,
        }
    '''
    pfx_len = len(path)
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            full_name = os.path.join(dirpath, filename)
            stat = os.stat(full_name)
            yield {
                'name': filename,
                'path': full_name[pfx_len:],
                'content_type': mimetypes.guess_type(full_name)[0],
                'size': stat.st_size,
                'modified': stat.st_mtime,
            }
