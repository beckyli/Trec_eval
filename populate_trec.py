__author__ = 'james'
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "trec_project.settings")

import django
django.setup()

from trec.models import *
from trec_project.settings import STATIC_PATH


def populate():
    add_researcher(uname="ASU",
                   disName="Alpha Team",
                   org="AS University")

    add_researcher(uname="CK",
                   disName="Chaos and Kontrol",
                   org="CK university")

    add_researcher(uname="HK",
                   disName="HongKongIR",
                   org="HK University")

    add_researcher(uname="ICT",
                   disName="ICTer",
                   org="University of ICT")

    add_researcher(uname="RIM",
                   disName="IRJobs",
                   org="Royal Insitute of Mayhem")

    rob2004 = add_track(tit="Robust2004",
                        url="http://trec.nist.gov/data/t13_robust.html",
                        desc="News Retrieval",
                        g="News")

    rob2005 = add_track(tit="Robust2005",
                        url="http://trec.nist.gov/data/t14_robust.html",
                        desc="News Retrieval",
                        g="News")

    million = add_track(tit="MillionQuery",
                        url="http://ciir.cs.umass.edu/research/million/",
                        desc="Million Query Track",
                        g="Web")

    tera = add_track(tit="Terabyte",
                     url="http://www-nlpir.nist.gov/projects/terabyte/",
                     desc="Terabyte Web Track",
                     g="Web")

    apnews = add_track(tit="APNews",
                       desc="News Retrieval Track",
                       g="News")

    add_task(trac=rob2005,
             tit="Ad Hoc Topic Retrieval",
             url="http://trec.nist.gov/data/t14_robust.html",
             desc="For each topic find all the relevant documents",
             y="2005",
             judge=open(os.path.join(STATIC_PATH, "robust", "aq.trec2005.qrels")))

    add_task(trac=tera,
             tit="Ad Hoc Topic Retrieval",
             url="http://www-nlpir.nist.gov/projects/terabyte/",
             desc="Ad Hoc Topic Retrieval",
             y="2005",
             judge=open(os.path.join(STATIC_PATH, "web", "dg.trec.qrels")))

    add_task(trac=apnews,
             tit="Ad Hoc Topic Retrieval",
             desc="Find all the relevant news articles",
             y="2001",
             judge=open(os.path.join(STATIC_PATH, "news", "ap.trec.qrels")))


    # Print out what we have added to the user.
    for r in Researcher.objects.all():
        print "- {0}".format(str(r))

    for track in Track.objects.all():
        for task in Task.objects.filter(track=track):
            print "- {0} - {1}".format(str(track), str(task))


def add_researcher(uname, disName="", org="", proPic=os.path.join(STATIC_PATH, "images", "avatars", "default.png"), web=""):
    r = Researcher.objects.get_or_create(username=uname)[0]
    r.profile_pic = proPic
    r.website = web
    r.displayName = disName
    r.organisation = org
    r.save()

    return r


def add_track(tit, desc="", g="", url=""):
    t = Track.objects.get_or_create(title=tit)[0]
    t.track_url = url
    t.description = desc
    t.genre = g
    t.save()

    return t


def add_task(trac, tit, url="", desc="", y="", judge=None):
    t = Task.objects.get_or_create(title=tit, track=trac)[0]
    t.task_url = url
    t.description = desc
    t.year = y
    t.judgement_file = judge
    t.save()

    return t


# Start execution here!
if __name__ == '__main__':
    print "Starting TREC population script..."
    populate()
