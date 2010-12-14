from openquake.faults.models import Fault, FaultSection
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.forms.models import ModelForm

class SectionInlineForm(ModelForm):
    class Meta:
        fields = ('upper_depth', 'lower_depth', 'geometry')

class SectionInline(admin.StackedInline): # TabularInline
    model = FaultSection
    extra = 1
    # formset = inlineformset_factory(Fault, FaultSection)
    form = SectionInlineForm

class FaultAdmin(OSMGeoAdmin): # admin.ModelAdmin
    # date_hierarchy = 'last_updated'
    list_display = ('name', 'completeness', 'last_updated')
    fieldsets = [
        (None,    {'fields': ['name']}), 
        ('Provenance', {'fields': 
                [('compiler', 'contributer'),
                'completeness', ], 'classes': ['collapse']}), 
        ('Details', {'fields': ['notes',],'classes': ['collapse']}),
    ]
    inlines = [SectionInline]


admin.site.register(Fault, FaultAdmin)