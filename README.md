# dumpling

## Setup

```
>>> pip install dumpling
```

Add `dumpling` to your `INSTALLED_APPS`

Add a setting `USER_TEMPLATES_PATH`.  This is where through-the-web (TTW) editable template files will live.

Add this value to the DIRS list for one of your TEMPLATES configs.

Add urls:

```
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^_/', include('dumpling.manage.urls')),
    url(r'^', include('dumpling.urls', namespace='dumpling')),
]
```
