from openquake.faults.models import Fault, FaultSection, Recurrence, Event, Observation
from openquake.faults.models import Fold, FoldTrace
from django.contrib import admin
from django.contrib.gis.db import models
from django.contrib.gis.admin import OSMGeoAdmin
from olwidget.admin import GeoModelAdmin
from django.forms.models import ModelForm
from olwidget.forms import MapModelForm
from olwidget.fields import MapField, EditableLayerField, InfoLayerField
from olwidget.widgets import Map, EditableMap, EditableLayer, InfoLayer

from django.contrib.auth.decorators import permission_required


class ObservationInline(admin.StackedInline):
    """
    Basic admin form for entering observation points.
    
    .. todo:: Allow multiple points to be entered at once.

    """
    model = Observation
    extra = 1
    max_num = 1
    formfield_overrides = {
        models.PointField: {'widget': EditableMap(options={'geometry': 'point', 'zoom_to_data_extent' : False})},
    }
    readonly_fields = ['fault']


class SectionInline(admin.StackedInline):
    """Basic admin form for entering and editing Section Traces.
    
    .. todo:: Show underlying observation points as Info Layer.
    .. todo:: Nested inlines with Recurrence and Events.
    .. todo:: Set fault properly on creation.
    
    """
    model = FaultSection
    extra = 1
    max_num = 1
    formfield_overrides = {
        models.LineStringField: 
                {'widget': EditableMap(options={'geometry': 'linestring', 'layers' : ['google.satellite']})},
    }
    fieldsets = [
        (None,  {'fields': 
            [('fault',), ('expression', 'method', 'is_episodic', 'is_active')],}),
        ('Geometry', {'fields': 
            ['accuracy', 'aseismic_slip_factor', ('slip_type', 'slip_rate'),
            ('dip_angle', 'rake_angle', 'strike_angle'), 'geometry',
            ('upper_depth', 'lower_depth', 'downthrown_side', )], 
            'classes' : ['wide', 'show'],}),
        ('Details', {'fields': ['notes'], 
            'classes': ['collapse']}),
    ]
    readonly_fields = ['fault']


class FaultAdmin(GeoModelAdmin):
    """Main admin form for Faults, with inline forms for sections and points.
    
    .. todo:: Filter by active
    
    """
    list_map = ['traces','observations']
    list_display = ('name', 'completeness', 'last_updated', 'verified_by')
    list_filter = ['completeness', 'verified_by', 'compiler']
    search_fields = ['name', 'notes']
    fieldsets = [
         (None,    {'fields': ['name']}), 
         ('Provenance', {'fields': 
                 [('compiler', 'contributer'),
                 'completeness', ], 'classes': ['collapse']}), 
         ('Details', {'fields': 
                ['notes',],'classes': ['collapse']}),
    ]
    actions = ['make_verified']
    inlines = [SectionInline, ObservationInline]

    def make_verified(self, request, queryset): 
        if request.user.has_perm('faults.can_verify_faults'):
            rows_updated = queryset.update(verified_by=request.user)
            if rows_updated == 1:
                message_bit = "1 fault was" 
            else:
                message_bit = "%s faults were" % rows_updated
            self.message_user(request, "%s successfully marked as verified." % message_bit)
        else:
            self.message_user(request, "You're not allowed to verify faults, sorry.")
    make_verified.short_description = "Mark selected faults as verified"


class TraceInline(admin.StackedInline):
    model = FoldTrace
    extra = 1
    max_num = 1
    formfield_overrides = {
        models.LineStringField: 
                {'widget': EditableMap(options={'geometry': 'linestring',})},
    }
    fieldsets = [
        (None,  {'fields': 
            [('fold',), ('expression', 'method', 'is_episodic', 'is_active')],}),
        ('Geometry', {'fields': 
            ['accuracy', 'geometry', ], 
            'classes' : ['wide', 'show'],}),
        ('Details', {'fields': ['notes'], 
            'classes': ['collapse']}),
    ]
    readonly_fields = ['fold']


class FoldAdmin(GeoModelAdmin):
    """Admin form to manage Folds, with inline for fold traces.
    .. todo:: Generalize fieldset and actions for Faults and Folds.
    """
    list_map = ['traces']
    list_display = ('name', 'completeness', 'last_updated', 'verified_by')
    list_filter = ['completeness', 'verified_by', 'compiler']
    search_fields = ['name', 'notes']
    fieldsets = [
         (None,    {'fields': ['name']}), 
         ('Provenance', {'fields': 
                 [('compiler', 'contributer'),
                 'completeness', ], 'classes': ['collapse']}), 
         ('Details', {'fields': 
                ['notes',],'classes': ['collapse']}),
    ]
    actions = ['make_verified']
    inlines = [TraceInline,]

    def make_verified(self, request, queryset): 
        if request.user.has_perm('faults.can_verify_folds'):
            rows_updated = queryset.update(verified_by=request.user)
            if rows_updated == 1:
                message_bit = "1 fold was" 
            else:
                message_bit = "%s folds were" % rows_updated
            self.message_user(request, "%s successfully marked as verified." % message_bit)
        else:
            self.message_user(request, "You're not allowed to verify folds, sorry.")
    make_verified.short_description = "Mark selected folds as verified"


class RecurrenceInline(admin.StackedInline):
    model = Recurrence
    extra = 0
    max_num = 1


class EventInline(admin.StackedInline):
    model = Event
    extra = 0
    

class FaultSectionAdmin(GeoModelAdmin):
    list_display = ('fault', 'id',)
    list_filter = ['fault']
    list_map = ['geometry']
    list_map_options = {
        # group nearby points into clusters
        # 'cluster': True,
        # 'cluster_display': 'list',
    }
    inlines = [RecurrenceInline, EventInline]
    fieldsets = [
        (None,  {'fields': 
            [('fault',), ('expression', 'method', 'is_episodic', 'is_active')],}),
        ('Geometry', {'fields': 
            ['accuracy', 'aseismic_slip_factor', ('slip_type', 'slip_rate'),
            ('dip_angle', 'rake_angle', 'strike_angle'), 'geometry',
            ('upper_depth', 'lower_depth', 'downthrown_side', )], 'classes' : ['wide', 'show'],}),
        ('Details', {'fields': ['notes'], 'classes': ['collapse']}),
    ]
    # OSMAdmin options
    # map_width = 700
    # map_height = 325
    
    # OLWidget Options
    options = {
        'default_lat': -72,
        'default_lon': 43,
    }
    # maps = (
    #     (('capital', 'perimiter'), { 'layers': ['google.streets'] }),
    #     (('biggest_river',), {'overlay_style': {'stroke_color': "#0000ff"}}),
    # )


admin.site.register(Fault, FaultAdmin)
admin.site.register(Fold, FoldAdmin)
admin.site.register(FaultSection, FaultSectionAdmin)