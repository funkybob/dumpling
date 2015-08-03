# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import dumpling.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dumpling', '0003_auto_20150513_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='template',
            field=dumpling.fields.RelativePathField(path='/home/curtis/src/git/dumpling/proj/templates/', recursive=True),
        ),
        migrations.AlterField(
            model_name='pagewidget',
            name='template',
            field=models.FilePathField(blank=True, path='/home/curtis/src/git/dumpling/proj/templates/', recursive=True),
        ),
    ]
