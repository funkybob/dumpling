# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import dumpling.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dumpling', '0002_auto_20150413_0830'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThemeManager',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ThemeValue',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('group', models.CharField(max_length=64, validators=[django.core.validators.RegexValidator('^\\w+$')])),
                ('name', models.CharField(max_length=64, validators=[django.core.validators.RegexValidator('^\\w+$')])),
                ('value', models.CharField(max_length=1024, blank=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='pagewidget',
            name='name',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='template',
            field=dumpling.fields.RelativePathField(path='/Users/curtis/src/git/dumpling/proj/templates/', recursive=True),
        ),
        migrations.AlterField(
            model_name='pagewidget',
            name='template',
            field=models.FilePathField(blank=True, recursive=True, path='/Users/curtis/src/git/dumpling/proj/templates/'),
        ),
        migrations.AlterUniqueTogether(
            name='pagewidget',
            unique_together=set([('page', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='themevalue',
            unique_together=set([('group', 'name')]),
        ),
    ]
