from django import template
from trec.models import *

register = template.Library()

@register.inclusion_tag('trec/table.html')
def get_results_list(arg):

    if hasattr(arg, 'user'):
        return {'headers': [['Track', 'task__track__title'], ['Task', 'task__title'], ['Name', 'name'],
                            ['M.A.P', 'map'], ['P10', 'p10'], ['P20', 'p20']],
                'rows': Run.objects.filter(researcher=arg),
                'results_for': arg.user.username,
                'researcher': True,
                'direction': 'ascending'
                }
    elif hasattr(arg, 'track'):
        return {'headers': [['Reseacher', 'researcher'], ['Name', 'name'],
                            ['M.A.P', 'map'], ['P10', 'p10'], ['P20', 'p20']],
                'rows': Run.objects.filter(task=arg),
                'results_for': arg.title,
                'task': True,
                'direction': 'ascending'
                }