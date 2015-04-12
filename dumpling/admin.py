from django.contrib import admin

from . import models


class PageAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'is_published',)
    list_filter = ('is_published',)

admin.site.register(models.Page, PageAdmin)
