from django.contrib.auth.models import User
from django.db import models

class Researcher(models.Model):

    user = models.OneToOneField(User)
    profile_pic = models.ImageField(upload_to='profile_images', blank=True)
    website = models.URLField(blank=True)
    display_name = models.CharField(max_length=128)
    organisation = models.CharField(max_length=128, blank=True)

    def __unicode__(self):
        return self.user.username

class Track(models.Model):

    title = models.CharField(max_length=128, unique=True)
    track_url = models.URLField()
    description = models.CharField(max_length=1024)
    genre = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.title

class Task(models.Model):

    track = models.ForeignKey(Track)
    title = models.CharField(max_length=128, unique=True)
    task_url = models.URLField()
    description = models.CharField(max_length=1024)
    year = models.TimeField()
    judgement_file = models.FileField(upload_to='judgement_files')

    def __unicode__(self):
        return self.title

class Run(models.Model):

    researcher = models.ForeignKey(Researcher)
    task = models.ForeignKey(Task)
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1024)
    results_file = models.FileField(upload_to='results')
    map = models.FloatField(null=True)
    p10 = models.FloatField(null=True)
    p20 = models.FloatField(null=True)

    run_types = (
        ("a", "Automatic"),
        ("m", "Manual"),
    )
    run_type = models.CharField(max_length=1, choices=run_types)

    query_types = (
        ("title", "Title"),
        ("ti+des", "Title and description"),
        ("dscrp", "Description"),
        ("all", "All"),
        ("other", "Other"),
    )
    query_type = models.CharField(max_length=6, choices=query_types)

    feedback_types = (
        ("none", "None"),
        ("pseud", "Pseudo"),
        ("rel", "Relevance"),
        ("other", "Other")
    )
    feedback_type = models.CharField(max_length=5, choices=feedback_types)

    def __unicode__(self):
        return self.name
