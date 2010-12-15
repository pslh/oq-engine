from openquake.faults.models import Fault, FaultSection, Recurrence
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.forms.models import ModelForm

class SectionInlineForm(ModelForm):
    class Meta:
        fields = ('upper_depth', 'lower_depth', 'geometry')

class SectionInline(admin.StackedInline): # TabularInline
    model = FaultSection
    extra = 0
    # formset = inlineformset_factory(Fault, FaultSection)
    form = SectionInlineForm

class RecurrenceInline(admin.StackedInline):
    model = Recurrence
    extra = 0
    
def make_verified(modeladmin, request, queryset): 
    queryset.update(verified_by=request.user)
make_verified.short_description = "Mark selected faults as verified"

class FaultAdmin(admin.ModelAdmin): # admin.ModelAdmin
    # date_hierarchy = 'last_updated'
    list_display = ('name', 'completeness', 'last_updated', 'verified_by')
    list_filter = ['completeness', 'verified_by', 'compiler']
    search_fields = ['name', 'notes']
    fieldsets = [
         (None,    {'fields': ['name']}), 
         ('Provenance', {'fields': 
                 [('compiler', 'contributer'),
                 'completeness', ], 'classes': ['collapse']}), 
         ('Details', {'fields': 
                ['downthrown_side', 'notes',],'classes': ['collapse']}),
    ]
    actions = [make_verified]
    # inlines = [SectionInline]

class FaultSectionAdmin(OSMGeoAdmin):
    list_filter = ['fault']
    inlines = [RecurrenceInline]
    readonly_fields = ['fault']
    fieldsets = [
        (None,  {'fields': 
            [('fault',), ('expression', 'method', 'is_episodic', 'is_active')],}),
        ('Geometry', {'fields': 
            ['accuracy', 'aseismic_slip_factor', ('slip_type', 'slip_rate'),
            ('dip_angle', 'rake_angle', 'strike_angle'), 'geometry',
            ('upper_depth', 'lower_depth')], 'classes' : ['wide', 'show'],}),
        ('Details', {'fields': ['notes'], 'classes': ['collapse']}),
    ]


admin.site.register(Fault, FaultAdmin)
admin.site.register(FaultSection, FaultSectionAdmin)