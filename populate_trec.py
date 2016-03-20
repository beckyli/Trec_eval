import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "trec_project.settings")

import django
django.setup()
from django.core.files import File

from trec.models import *
from trec_project.settings import MEDIA_ROOT

def populate():
    add_researcher(uname="ASU",
                   dis_name="Alpha Team",
                   org="AS University")

    add_researcher(uname="CK",
                   dis_name="Chaos and Kontrol",
                   org="CK university")

    add_researcher(uname="HK",
                   dis_name="HongKongIR",
                   org="HK University")

    add_researcher(uname="ICT",
                   dis_name="ICTer",
                   org="University of ICT")

    add_researcher(uname="RIM",
                   dis_name="IRJobs",
                   org="Royal Insitute of Mayhem")

    for name in ['jill', 'jim', 'joe', 'bob', 'jen']:
        add_researcher(name)

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
             judge=os.path.join(MEDIA_ROOT, "judgement_files", "aq.trec2005.qrels"))

    add_task(trac=tera,
             tit="Ad Hoc Topic Retrieval",
             url="http://www-nlpir.nist.gov/projects/terabyte/",
             desc="Ad Hoc Topic Retrieval",
             y="2005",
             judge=os.path.join(MEDIA_ROOT, "judgement_files", "dg.trec.qrels"))

    add_task(trac=apnews,
             tit="Ad Hoc Topic Retrieval",
             desc="Find all the relevant news articles",
             y="2001",
             judge=os.path.join(MEDIA_ROOT, "judgement_files", "ap.trec.qrels"))

    # Print out what we have added to the user.
    for r in Researcher.objects.all():
        print "- {0}".format(str(r))

    for track in Track.objects.all():
        for task in Task.objects.filter(track=track):
            print "- {0} - {1}".format(str(track), str(task))

def add_researcher(uname, pro_pic=None, dis_name="", org="", web=""):
    u = User.objects.get_or_create(username=uname)[0]
    u.set_password(uname)
    u.save()
    r = Researcher.objects.get_or_create(user=u)[0]
    r.profile_pic = pro_pic
    r.website = web
    r.display_name = dis_name
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
    if judge:
        t.judgement_file = File(open(judge))
    t.save()
    return t

# Start execution here!
if __name__ == '__main__':
    print "Starting TREC population script..."
    populate()
