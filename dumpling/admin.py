from django.contrib import admin

from django_hstore.widgets import AdminHStoreWidget

from . import models


class PageWidgetInline(admin.TabularInline):
    model = models.PageWidget


class PageAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'is_published',)
    list_filter = ('is_published',)
    inlines = [
        PageWidgetInline,
    ]
    formfield_overrides = {
        models.HStoreField: {'widget': AdminHStoreWidget},
    }
    fieldsets = (
        (None, {
            'fields': (
                ('parent', 'path'),
                'title',
                'template',
                ('is_published', 'order'),
                'fragments',
            ),
        }),
    )


admin.site.register(models.Page, PageAdmin)
admin.site.register(models.PageWidget)


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'value', 'description')
    list_filter = ('group',)
    list_editable = ('value',)
    ordering = ('group', 'name',)
    fieldsets = (
        (None, {
            'fields': (
                ('group', 'name', 'value',),
                'description',
            ),
        }),
    )

admin.site.register(models.ThemeValue, ThemeAdmin)
