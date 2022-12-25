from django.contrib import admin
from .models import *

class task(admin.ModelAdmin):
    raw_id_fields=('team_assign', 'assigned_by') 
class team(admin.ModelAdmin):
    raw_id_fields=('belongs_to',)
class assign(admin.ModelAdmin):
    raw_id_fields=('task', 'assgined_to')

admin.site.register(Task,task)
admin.site.register(AssignedTo,assign)
admin.site.register(Team,team)
# Register your models here.
