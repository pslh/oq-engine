from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
from django.contrib import databrowse

from openquake.faults import models

databrowse.site.register(models.Fault)
databrowse.site.register(models.FaultSection)

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^openquakeweb/', include('openquakeweb.foo.urls')),
    (r'^databrowse/(.*)', databrowse.site.root),
    (r'^admin/', include(admin.site.urls)),
    (r'^', direct_to_template, {'template': 'welcome.html'}),
)
