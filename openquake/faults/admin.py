from openquake.faults.models import Fault, FaultSection, Recurrence, Event, Observation
from django.contrib import admin
from django.contrib.gis.db import models
from django.contrib.gis.admin import OSMGeoAdmin
from olwidget.admin import GeoModelAdmin
from django.forms.models import ModelForm
from olwidget.forms import MapModelForm
from olwidget.fields import MapField, EditableLayerField, InfoLayerField
from olwidget.widgets import Map, EditableMap, EditableLayer, InfoLayer

from django.contrib.auth.decorators import permission_required

class SectionInlineForm(ModelForm):
    layers = [EditableLayerField({'geometry': 'linestring', 'name': 'geometry'})]
    # geometry = EditableLayerField({'overlay_style': { 'fill_color': "#ff0000" }})
    # layers.append(InfoLayerField([[c.geometry, "foo"] for c in FaultSection.objects.all() if c.geometry],
    #         {
    #             'overlay_style': {
    #                 'fill_opacity': 0,
    #                 'stroke_color': "white",
    #                 'stroke_width': 6,
    #             }, 
    #             'name': "Country boundaries",
    #         }))
    # info_layer_field = InfoLayerField([[x.geometry.wkt, "something %s" % x] for x in Fault.objects.all() if x.geometry is not None  ] , {'name': "Other Sections"})
    # layers.extend([InfoLayerField([[x.geometry.wkt, "something"]], {'name': "Other Sections"}) for x in Fault.objects.all() if x.geometry is not None])
    geometry = MapField(layers, {
            'overlay_style': {
                'fill_color': '#00ff00',
            },
            'layers' : ['osm.osmarender'],
        })
    class Meta:
        pass
# 
# class EditableLineStringMap(EditableMap):
#     options = {'geometry': 'linestring'}


class ObservationInline(admin.StackedInline):
    model = Observation
    extra = 1
    max_num = 1
    formfield_overrides = {
        models.PointField: {'widget': EditableMap(options={'geometry': 'point', 'zoom_to_data_extent' : False})},
    }
    readonly_fields = ['fault']


class SectionInline(admin.StackedInline): # TabularInline
    model = FaultSection
    extra = 1
    max_num = 1
    # formset = inlineformset_factory(Fault, FaultSection)
    # form = SectionInlineForm
    formfield_overrides = {
        models.LineStringField: {'widget': EditableMap(options={'geometry': 'linestring',})}, #  'hide_textarea' : False
        # models.LineStringField: {'widget': Map(
        #               vector_layers=[EditableLayer(options={'geometry': 'linestring', 'name': 'geometry'}),
        #                              InfoLayer(info=[[c.geometry, "foo"] for c in FaultSection.objects.all() if c.geometry])], options={'name' : 'reference_geometry'}) },
    }
    fieldsets = [
        (None,  {'fields': 
            [('fault',), ('expression', 'method', 'is_episodic', 'is_active')],}),
        ('Geometry', {'fields': 
            ['accuracy', 'aseismic_slip_factor', ('slip_type', 'slip_rate'),
            ('dip_angle', 'rake_angle', 'strike_angle'), 'geometry',
            ('upper_depth', 'lower_depth', 'downthrown_side', )], 'classes' : ['wide', 'show'],}),
        ('Details', {'fields': ['notes'], 'classes': ['collapse']}),
    ]
    readonly_fields = ['fault']


class FaultAdmin(GeoModelAdmin): # admin.ModelAdmin
    # date_hierarchy = 'last_updated'
    list_map = ['geometry']
    list_map_options = {
        # group nearby points into clusters
        # 'cluster': True,
        # 'cluster_display': 'list',
    }
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
admin.site.register(FaultSection, FaultSectionAdmin)