from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from scss import Compiler
from scss.namespace import Namespace
from scss.types import String

from .models import Page, ThemeValue


class PageView(DetailView):
    context_object_name = 'page'

    def get_queryset(self):
        return Page.objects.published().prefetch_related('pagewidget_set__widget')

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        paths = list(filter(None, self.kwargs.get('path', '/').split('/')))

        if not paths:
            paths = ['']

        paths.reverse()

        query = {}
        prefix = 'path'
        for step in paths:
            query[prefix] = step
            prefix = 'parent__' + prefix
        query[prefix.replace('path', 'isnull')] = True

        return get_object_or_404(queryset, **query)

    def get_template_names(self):
        return self.object.template[len(settings.USER_TEMPLATES_PATH):]


def styles(request, name):
    src = ''
    namespace = Namespace()
    for tv in ThemeValue.objects.all():
        namespace.set_variable('${}-{}'.format(tv.group, tv.name), String(tv.value))
    compiler = Compiler(namespace=namespace)
    return HttpResponse(compiler.compile_string(src), content_type='text/css')
