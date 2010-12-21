import functools

import olwidget

from models import FaultSection, Fault, Observation
from django import forms
from django.forms.models import ModelForm
from django.contrib.admin.helpers import InlineAdminForm, AdminForm

from olwidget.forms import MapModelForm
from olwidget.fields import MapField, EditableLayerField, InfoLayerField
from olwidget.widgets import EditableLayer, InfoLayer, Map

from django.contrib.gis.db.models.fields import LineStringField

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.formtools.wizard import FormWizard

from openquake.faults import classmaker


MAP_OPTIONS = {
        'default_lat' : -41.215,
        'default_lon' : 174.897, 
        'default_zoom' : 10,
        'layers' : ['google.satellite', 've.aerial', 'osm.osmarender'],
        'zoom_to_data_extent' : True,
        'popups_outside' : True,
        'map_options' : { 
                'controls' : 
                ['LayerSwitcher', 'Navigation', 'PanZoomBar', 'Attribution'], 
                'min_extent' : 'new OpenLayers.Bounds(-10, -10, 10, 10)'},
        'min_extent' : 'new OpenLayers.Bounds(-10, -10, 10, 10)',
        
}


class FaultForm(ModelForm):
    """Main form for editing existing Faults."""
    class Meta:
        model = Fault


class FaultCreationForm(ModelForm):
    """A form that creates a Fault, with no sections."""
    name = forms.CharField(label=_("Name of Fault"))

    class Meta:
        model = Fault
        fields = ("name",)

    def save(self, commit=True):
        fault = super(FaultCreationForm, self).save(commit=False)
        if commit:
            fault.save()
        return fault


class SectionForm(ModelForm, MapModelForm):
    """FaultSection creation and editing, used both in dedicated and inline views."""
    __metaclass__ = classmaker()

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        layers = [EditableLayerField({'geometry': 'linestring', 'name': 'geometry'})]
        traces = []
        points = []
        if hasattr(self.instance, 'fault'):
            for section in self.instance.fault.faultsection_set.filter(
                    geometry__isnull=False).all():
                    traces.append([section.geometry, 
                        "%s Sections" % (section.__unicode__())])            
            for observed in self.instance.fault.observation_set.filter(
                    geometry__isnull=False).all():
                    points.append([observed.geometry, 
                        "%s Observations" % (observed.__unicode__())])
        if traces:
            layers.append(InfoLayerField(traces,
                        {
                            'geometry': 'linestring',
                            'overlay_style': {
                                'fill_opacity': 0,
                                'stroke_color': "grey",
                                'stroke_width': 1,
                            }, 
                            'name': "Other Sections",
                        }))         
        if points:
            layers.append(InfoLayerField(points,
                        {
                            'geometry': 'point',
                            'overlay_style': {                             
                                'externalGraphic': "/media/alien.png",
                                'graphicWidth': 21,
                                'graphicHeight': 25,
                            }, 
                            'name': "Observations",
                        }))   

        self.fields['geometry'] = olwidget.fields.MapField(layers, MAP_OPTIONS)

    class Meta:
        model = FaultSection
        fieldsets = [
            (None,  {'fields': 
                [('fault',), ('expression', 'method', 'is_episodic', 'is_active')],}),
            ('Geometry', {'fields': 
                ['accuracy', 'aseismic_slip_factor', ('slip_type', 'slip_rate'),
                ('dip_angle', 'rake_angle', 'strike_angle'), 'geometry',
                ('upper_depth', 'lower_depth', 'downthrown_side', )], 'classes' : ['wide', 'show'],}),
            ('Details', {'fields': ['notes'], 'classes': ['collapse']}),
        ]


class SectionInlineForm(InlineAdminForm, SectionForm):
    __metaclass__ = classmaker()


class ObservationForm(ModelForm, MapModelForm):
    __metaclass__ = classmaker()
    
    def __init__(self, *args, **kwargs):
        super(ObservationForm, self).__init__(*args, **kwargs)
        layers = [EditableLayerField({'geometry': 'point', 'name': 'geometry'})]
        traces = []
        points = []
        if hasattr(self.instance, 'fault'):
            for section in self.instance.fault.faultsection_set.filter(
                    geometry__isnull=False).all():
                    traces.append([section.geometry, 
                        "%s Sections" % (section.__unicode__())])            
            for observed in self.instance.fault.observation_set.filter(
                    geometry__isnull=False).all():
                    points.append([observed.geometry, 
                        "%s Observations" % (observed.__unicode__())])
        if traces:
            layers.append(InfoLayerField(traces,
                        {
                            'geometry': 'linestring',
                            'overlay_style': {
                                'fill_opacity': 0,
                                'stroke_color': "grey",
                                'stroke_width': 1,
                            }, 
                            'name': "Other Sections",
                        }))         
        if points:
            layers.append(InfoLayerField(points,
                        {
                            'geometry': 'point',
                            'overlay_style': {                             
                                'externalGraphic': "/media/alien.png",
                                'graphicWidth': 21,
                                'graphicHeight': 25,
                            }, 
                            'name': "Observations",
                        }))   

        self.fields['geometry'] = olwidget.fields.MapField(layers, MAP_OPTIONS)
    
    class Meta:
        model = Observation
        fieldsets = [
            (None,  {'fields': [ 'geometry','notes'], 'classes' : ['wide', 'show'],}),
        ]
        

class FaultWizard(FormWizard):
        
    def done(self, request, form_list):
        for form in form_list:
            if form.is_valid():
                form.save()
        #self.do_something_with_the_form_data([form.cleaned_data for form in form_list])
        return HttpResponseRedirect('/page-to-redirect-to-when-done/')