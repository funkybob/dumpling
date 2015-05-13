
from nap.datamapper import field, Field, ModelDataMapper

from . import models


class PageMapper(ModelDataMapper):

    class Meta:
        model = models.Page
        fields = '__all__'
