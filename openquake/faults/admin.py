from openquake.faults.models import Fault, FaultSection
from django.contrib import admin

class SectionInline(admin.TabularInline): 
    model = FaultSection
    extra = 1

class FaultAdmin(admin.ModelAdmin):
    inlines = [SectionInline]
    list_display = ('name',)
    # fieldsets = [
    #     (None,    {'fields': ['question']}), 
    #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    # ]


admin.site.register(Fault, FaultAdmin)