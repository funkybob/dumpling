
from django.conf import settings
from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property


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
    template = models.FilePathField(path=settings.USER_TEMPLATES_PATH,
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

    def __getitem__(self, key):
        return self.fragments[key]
