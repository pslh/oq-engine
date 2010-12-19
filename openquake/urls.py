from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.static import serve

from django.contrib import admin
from django.contrib import databrowse

from openquake.faults import models
from openquake.faults.forms import SectionForm, FaultForm, FaultWizard

databrowse.site.register(models.Fault)
databrowse.site.register(models.FaultSection)
databrowse.site.register(models.Observation)
databrowse.site.register(models.Fold)
databrowse.site.register(models.FoldTrace)

admin.autodiscover()

urlpatterns = patterns('',
    (r'^faults/add$', FaultWizard([FaultForm, SectionForm])),
    (r'^faults/edit/(?P<fault_id>.*)/$', FaultWizard([FaultForm, SectionForm])),
    (r'^databrowse/(.*)', databrowse.site.root),
    (r'^admin/', include(admin.site.urls)),
    (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 
            serve, {'document_root': settings.MEDIA_ROOT}), 
    (r'^', direct_to_template, {'template': 'welcome.html'}),
)
