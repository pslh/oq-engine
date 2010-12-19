from models import FaultSection, Fault, Observation
from django import forms
from django.forms.models import ModelForm
from olwidget.forms import MapModelForm
from olwidget.fields import EditableLayerField

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.formtools.wizard import FormWizard
from olwidget.fields import MapField, EditableLayerField, InfoLayerField

from openquake.faults import classmaker

class FaultForm(ModelForm):    
    class Meta:
        model = Fault


class FaultCreationForm(ModelForm):
    """
    A form that creates a Fault, with no sections.
    """
    name = forms.CharField(label=_("Name of Fault"))

    class Meta:
        model = Fault
        fields = ("name",)

    def save(self, commit=True):
        fault = super(FaultCreationForm, self).save(commit=False)
        if commit:
            fault.save()
        return fault

MAP_OPTIONS = {
        'default_lat' : -41.215,
        'default_lon' : 174.897, 
        'default_zoom' : 10,
        'layers' : ['google.satellite', 've.aerial', 'osm.osmarender'],
        'zoom_to_data_extent' : True,
        'popups_outside' : True,
}

class SectionForm(ModelForm, MapModelForm):
    __metaclass__ = classmaker()
    layers = [EditableLayerField({'geometry': 'linestring', 'name': 'geometry'})]
    layers.append(InfoLayerField([[c.geometry, c.__unicode__()] for c in Observation.objects.filter(geometry__isnull=False)],
            {
                'overlay_style': {
                    'fill_opacity': 0,
                    'stroke_color': "black",
                    'stroke_width': 4,
                }, 
                'name': "Observations",
            }))    
    layers.append(InfoLayerField([[c.geometry, c.__unicode__()] for c in FaultSection.objects.filter(geometry__isnull=False)],
            {
                'overlay_style': {
                    'fill_opacity': 0,
                    'stroke_color': "black",
                    'stroke_width': 4,
                }, 
                'name': "Sections",
            }))
    geometry = MapField(layers, {
            'overlay_style': {
                'fill_color': '#00ff00',
            }, 'layers' : ['google.satellite'], 
        })
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


class ObservationForm(ModelForm, MapModelForm):
    __metaclass__ = classmaker()
    layers = [EditableLayerField({'geometry': 'point', 'name': 'geometry'})]
    layers.append(InfoLayerField([[c.geometry, c.__unicode__()] for c in Observation.objects.filter(geometry__isnull=False)],
            {
                'overlay_style': {
                    'fill_opacity': 0,
                    'stroke_color': "black",
                    'stroke_width': 4,
                }, 
                'name': "Observations",
            }))    
    geometry = MapField(layers, {
            'overlay_style': {
                'fill_color': '#00ff00',
            }, 'layers' : ['google.satellite'],
        })
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