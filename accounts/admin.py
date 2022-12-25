from django.contrib import admin
from .models import *

class guide(admin.ModelAdmin):
    list_display = ('user', 'committee', 'department')
    search_fields = ('user', 'committee', 'department')
    raw_id_fields=('user', 'committee')

class core_cocom(admin.ModelAdmin):
    list_display = ('user', 'position', 'committee', 'department')
    search_fields = ('user', 'position', 'committee', 'department')
    raw_id_fields=('user', 'position', 'committee') 

admin.site.register(User)
admin.site.register(Guide, guide)
admin.site.register(Core, core_cocom)
admin.site.register(CoCom, core_cocom)


class committee(admin.ModelAdmin):
    list_display = ('Committee_name','Committee_Department', 'Committee_date_of_establishment')
    search_fields = ('Committee_name',)

class position(admin.ModelAdmin):
    list_display = ('Position_name', 'Committee', 'Position_for')
    raw_id_fields=('Committee',)

admin.site.register(Committee, committee)
admin.site.register(Position, position)

