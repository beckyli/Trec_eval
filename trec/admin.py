from django.contrib import admin

from trec.models import *

# Add in this class to customized the Admin Interface
class ResearcherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('username',)}

class TrackAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class TaskAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Researcher, ResearcherAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Run)


