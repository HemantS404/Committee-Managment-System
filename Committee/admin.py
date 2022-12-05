from django.contrib import admin
from .models import *

class committee(admin.ModelAdmin):
    list_display = ('Committee_name','Committee_Department', 'Committee_date_of_establishment')
    search_fields = ('Committee_name',)

class position(admin.ModelAdmin):
    list_display = ('Position_name', 'Committee', 'Position_for')
    raw_id_fields=('Committee',)

admin.site.register(Committee, committee)
admin.site.register(Position, position)
# Register your models here.
