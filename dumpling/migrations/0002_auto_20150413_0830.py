# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import dumpling.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('dumpling', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageWidget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('template', models.FilePathField(recursive=True, path='/Users/curtis/env/holster/site_templates/')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.AlterField(
            model_name='page',
            name='template',
            field=dumpling.fields.RelativePathField(recursive=True, path='/Users/curtis/env/holster/site_templates/'),
        ),
        migrations.AddField(
            model_name='pagewidget',
            name='page',
            field=models.ForeignKey(to='dumpling.Page'),
        ),
        migrations.AlterUniqueTogether(
            name='pagewidget',
            unique_together=set([('page', 'template')]),
        ),
    ]
