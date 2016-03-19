# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trec', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='results_file',
            field=models.FileField(upload_to=b'C:\\Users\\YS15102488\\code\\trec-eval\\media\\results'),
        ),
        migrations.AlterField(
            model_name='task',
            name='judgement_file',
            field=models.FileField(upload_to=b'C:\\Users\\YS15102488\\code\\trec-eval\\media\\judgement_files'),
        ),
    ]
