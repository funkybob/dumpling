
from django.db.models.fields import FilePathField

from . import forms


class RelativePathField(FilePathField):
    description = 'relative path'

    def form_field(self, **kwargs):
        kwargs.setdefault('form_class', forms.RelativePathField)
        return super(RelativePathField, self).form_field(**kwargs)
