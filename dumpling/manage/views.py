from django.shortcuts import render

from ..models import Page


def index(request):
    return render(request, 'dumpling/index.html', {
        'roots': Page.objects.filter(parent=None),
    })
