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


class SectionForm(ModelForm, MapModelForm):
    __metaclass__ = classmaker()
    # geom1 = EditableLayerField({'overlay_style': { 'fill_color': "#ff0000" }})
    layers = [EditableLayerField({'geometry': 'linestring', 'name': 'geometry'})]
    layers.append(InfoLayerField([[c.geometry, c.__unicode__()] for c in Observation.objects.filter(geometry__isnull=False)],
            {
                'overlay_style': {
                    'fill_opacity': 0,
                    'stroke_color': "white",
                    'stroke_width': 6,
                }, 
                'name': "Observations",
            }))
    # info_layer_field = InfoLayerField([[x.geometry.wkt, "something %s" % x] for x in Fault.objects.all() if x.geometry is not None  ] , {'name': "Other Sections"})
    # layers.extend([InfoLayerField([[x.geometry.wkt, "something"]], {'name': "Other Sections"}) for x in Fault.objects.all() if x.geometry is not None])
    geometry = MapField(layers, {
            'overlay_style': {
                'fill_color': '#00ff00',
            },
        })
    class Meta:
        model = FaultSection
        # fields = ('upper_depth', 'lower_depth', 'geometry')
        # exclude = ('geometry',)
        fieldsets = [
            (None,  {'fields': 
                [('fault',), ('expression', 'method', 'is_episodic', 'is_active')],}),
            ('Geometry', {'fields': 
                ['accuracy', 'aseismic_slip_factor', ('slip_type', 'slip_rate'),
                ('dip_angle', 'rake_angle', 'strike_angle'), 'geometry',
                ('upper_depth', 'lower_depth', 'downthrown_side', )], 'classes' : ['wide', 'show'],}),
            ('Details', {'fields': ['notes'], 'classes': ['collapse']}),
        ]
        #readonly_fields = ['fault']
        # options = { 'layers': ['google.streets'] }
        
        # maps = (
        #     (('geom1', 'geom2'), { 'layers': ['google.streets'] }),
        #     (('geom3', ), None),
        # )
        # fieldsets = [
        #     (None,  {'fields': 
        #         [('fault',), ('expression', 'method', 'is_episodic', 'is_active')],}),
        #     ('Geometry', {'fields': 
        #         ['accuracy', 'aseismic_slip_factor', ('slip_type', 'slip_rate'),
        #         ('dip_angle', 'rake_angle', 'strike_angle'), 'geometry',
        #         ('upper_depth', 'lower_depth', 'downthrown_side', )], 'classes' : ['wide', 'show'],}),
        #     ('Details', {'fields': ['notes'], 'classes': ['collapse']}),
        # ]



class FaultWizard(FormWizard):
        
    def done(self, request, form_list):
        for form in form_list:
            if form.is_valid():
                form.save()
        #self.do_something_with_the_form_data([form.cleaned_data for form in form_list])
        return HttpResponseRedirect('/page-to-redirect-to-when-done/')