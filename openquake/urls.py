from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^openquakeweb/', include('openquakeweb.foo.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^', direct_to_template, {'template': 'welcome.html'}),
)
