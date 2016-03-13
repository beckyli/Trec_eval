from django.db import models

from trec_project.enumTypes import runTypes, feedbackTypes, queryTypes
from trec_project.settings import STATIC_PATH
from django.template.defaultfilters import slugify
import os


# Create your models here.

class Researcher(models.Model):

    username = models.CharField(max_length=128, unique=True, default="")
    profile_pic = models.FilePathField(max_length=1024)
    website = models.CharField(max_length=1024, default="")
    display_name = models.CharField(max_length=128, default="")
    organisation = models.CharField(max_length=128, default="")
    slug = models.SlugField(max_length=1024, default="")

    def save(self, *args, **kwargs):

        self.slug = slugify(self.username)
        super(Researcher, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.username

class Track(models.Model):

    title = models.CharField(max_length=128, unique=True)
    track_url = models.CharField(max_length=1024, default="")
    description = models.CharField(max_length=1024, default="")
    genre = models.CharField(max_length=1024, default="")
    slug = models.SlugField(max_length=1024, default="")

    def save(self, *args, **kwargs):

        self.slug = slugify(self.title)
        super(Track, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

class Task(models.Model):

    track = models.ForeignKey(Track)
    title = models.CharField(max_length=128, default="")
    task_url = models.CharField(max_length=1024, default="")
    description = models.CharField(max_length=1024)
    year = models.CharField(max_length=4, default="")
    judgement_file = models.FilePathField()
    slug = models.SlugField(max_length=1024, default="")

    def save(self, *args, **kwargs):

        self.slug = slugify(self.title)
        super(Task, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

class Run(models.Model):

    researcher = models.ForeignKey(Researcher)
    task = models.ForeignKey(Task)
    name = models.CharField(max_length=128, default="")
    description = models.CharField(max_length=1024, default="")
    results_file = models.FilePathField()
    map = models.FloatField()
    p10 = models.FloatField()
    p20 = models.FloatField()

    run_type = models.CharField(max_length=1, choices=runTypes, default=runTypes[0][0])


    query_type = models.CharField(max_length=6, choices=queryTypes, default=queryTypes[0][0])


    feedback_type = models.CharField(max_length=5, choices=feedbackTypes, default=feedbackTypes[0][0])

    def __unicode__(self):
        return self.name