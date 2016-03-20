# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_pic', models.ImageField(default=b'/home/james/Documents/Uni/WAD2/trec-eval/media/profile_pics/default.jpg', upload_to=b'/home/james/Documents/Uni/WAD2/trec-eval/media/profile_pics', blank=True)),
                ('website', models.URLField(default=b'', max_length=1024, blank=True)),
                ('display_name', models.CharField(default=b'', max_length=128)),
                ('organisation', models.CharField(default=b'', max_length=128, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=128)),
                ('description', models.CharField(default=b'', max_length=1024)),
                ('results_file', models.FileField(upload_to=b'/home/james/Documents/Uni/WAD2/trec-eval/media/results')),
                ('map', models.FloatField(null=True)),
                ('p10', models.FloatField(null=True)),
                ('p20', models.FloatField(null=True)),
                ('run_type', models.CharField(default=b'a', max_length=1, choices=[(b'a', b'Automatic'), (b'm', b'Manual')])),
                ('query_type', models.CharField(default=b'title', max_length=6, choices=[(b'title', b'Title'), (b'ti+des', b'Title and description'), (b'desc', b'Description'), (b'all', b'All'), (b'other', b'Other')])),
                ('feedback_type', models.CharField(default=b'none', max_length=5, choices=[(b'none', b'None'), (b'pseud', b'Pseudo'), (b'rel', b'Relevance'), (b'other', b'Other')])),
                ('researcher', models.ForeignKey(to='trec.Researcher')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=128)),
                ('task_url', models.URLField(default=b'', max_length=1024)),
                ('description', models.CharField(max_length=1024)),
                ('year', models.CharField(default=b'', max_length=4)),
                ('judgement_file', models.FileField(upload_to=b'/home/james/Documents/Uni/WAD2/trec-eval/media/judgement_files')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=128)),
                ('track_url', models.URLField(default=b'', max_length=1024)),
                ('description', models.CharField(default=b'', max_length=1024)),
                ('genre', models.CharField(default=b'', max_length=1024)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='task',
            name='track',
            field=models.ForeignKey(to='trec.Track'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='run',
            name='task',
            field=models.ForeignKey(to='trec.Task'),
            preserve_default=True,
        ),
    ]
