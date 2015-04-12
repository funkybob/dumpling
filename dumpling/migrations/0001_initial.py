# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.contrib.postgres.fields.hstore
from django.contrib.postgres.operations import HStoreExtension


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        HStoreExtension(),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('path', models.SlugField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(max_length=100)),
                ('fragments', django.contrib.postgres.fields.hstore.HStoreField(blank=True)),
                ('template', models.FilePathField(recursive=True, path='/home/curtis/venv/dumpling/holster/site_templates/')),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('is_published', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(to='dumpling.Page', null=True, blank=True, related_name='children')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('parent', 'path')]),
        ),
    ]
