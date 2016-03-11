from django.db import models

# Create your models here.

class Researcher(models.Model):

    username = models.CharField(max_length=128, unique=True)
    profile_pic = models.ImageField(name='avatar', width_field=200, height_field=200)
    website = models.CharField(max_length=1024)
    display_name = models.CharField(max_length=128)
    organisation = models.CharField(max_length=128)

    def __unicode__(self):
        return self.username

class Track(models.Model):

    title = models.CharField(max_length=128, unique=True)
    track_url = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    genre = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.title

class Task(models.Model):

    track = models.ForeignKey(Track)
    title = models.CharField(max_length=128, unique=True)
    task_url = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    year = models.TimeField()
    judgementFile = models.FileField()

    def __unicode__(self):
        return self.title

class Run(models.Model):

    researcher = models.ForeignKey(Researcher)
    task = models.ForeignKey(Task)
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1024)
    results_file = models.FileField()
    map = models.FloatField()
    p10 = models.FloatField()
    p20 = models.FloatField()

    runTypes = (
        ("a", "Automatic"),
        ("m", "Manual"),
    )
    runType = models.CharField(max_length=1, choices=runTypes)

    queryTypes = (
        ("title", "Title"),
        ("ti+des", "Title and description"),
        ("dscrp", "Description"),
        ("all", "All"),
        ("other", "Other"),
    )
    queryType = models.CharField(max_length=6, choices=queryTypes)

    feedbackTypes = (
        ("none", "None"),
        ("pseud", "Pseudo"),
        ("rel", "Relevance"),
        ("other", "Other")
    )
    feedbackType = models.CharField(max_length=5, choices=feedbackTypes)

    def __unicode__(self):
        return self.name