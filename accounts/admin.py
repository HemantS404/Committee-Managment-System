from django.contrib import admin
from Committee.models import *
from .models import *

class guide(admin.ModelAdmin):
    list_display = ('user', 'committee', 'department')
    search_fields = ('user', 'committee', 'department')
    raw_id_fields=('user', 'committee')

class core_cocom(admin.ModelAdmin):
    list_display = ('user', 'position', 'committee','SAPID', 'department')
    search_fields = ('user', 'position', 'SAPID', 'committee', 'department')
    raw_id_fields=('user', 'position', 'committee') 

admin.site.register(User)
admin.site.register(Guide, guide)
admin.site.register(Core, core_cocom)
admin.site.register(CoCom, core_cocom)