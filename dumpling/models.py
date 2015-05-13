from collections import defaultdict

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.postgres.fields import HStoreField
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from .fields import RelativePathField


class PageQuerySet(models.QuerySet):

    def published(self):
        return self.filter(is_published=True)


class Page(models.Model):
    # Tree fields
    parent = models.ForeignKey('self', blank=True, null=True,
                               related_name='children')
    path = models.SlugField(blank=True)
    order = models.PositiveIntegerField(default=0)

    # Content fields
    title = models.CharField(max_length=100)
    fragments = HStoreField(blank=True)
    template = RelativePathField(path=settings.USER_TEMPLATES_PATH,
                                 recursive=True)

    # Meta data
    created = models.DateTimeField(default=timezone.now, editable=False)
    is_published = models.BooleanField(default=False)

    # Use custom Manager/QuerySet
    objects = PageQuerySet.as_manager()

    class Meta:
        unique_together = (
            ('parent', 'path'),
        )

    def get_absolute_url(self):
        return self.url

    @cached_property
    def url(self):
        steps = [self.path]
        node = self
        while node.parent:
            node = node.parent
            steps.append(node.path)
        steps.reverse()
        return '/' + '/'.join(steps)

    @cached_property
    def widget(self):
        # How does this give access to the template?
        return {
            pw.name: pw.widget
            for pw in self.pagewidget_set.all()
        }

    def __getitem__(self, key):
        return self.fragments[key]


class PageWidget(models.Model):
    '''
    Binds a model to the page with a name.
    '''
    page = models.ForeignKey('Page')
    name = models.SlugField()
    template = models.FilePathField(path=settings.USER_TEMPLATES_PATH,
                                    blank=True, recursive=True)
    content_type = models.ForeignKey('contenttypes.ContentType')
    object_id = models.PositiveIntegerField()
    widget = GenericForeignKey()

    class Meta:
        unique_together = (
            ('page', 'name'),
        )


class ThemeManager(models.Model):

    def get_theme_values(self):
        qset = self.get_queryset().values_list('group', 'name', 'value')
        values = defaultdict(dict)
        for group, name, value in qset:
            values[group][name] = value
        return dict(values)


class ThemeValue(models.Model):
    '''
    Provides global context values.
    '''
    group = models.CharField(max_length=64, validators=[RegexValidator(r'^\w+$')])
    name = models.CharField(max_length=64, validators=[RegexValidator(r'^\w+$')])
    value = models.CharField(max_length=1024, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = (
            ('group', 'name'),
        )
