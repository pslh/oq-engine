from django.conf.urls.defaults import *
from django.contrib import databrowse

from openquake.faults import models
from openquake.faults.forms import SectionForm, FaultForm, FaultWizard

databrowse.site.register(models.Fault)
databrowse.site.register(models.FaultSection)
databrowse.site.register(models.Observation)
databrowse.site.register(models.Fold)
databrowse.site.register(models.FoldTrace)

urlpatterns = patterns('',
    (r'^faults/add$', FaultWizard([FaultForm, SectionForm])),
    (r'^faults/edit/(?P<fault_id>.*)/$', FaultWizard([FaultForm, SectionForm])),
)