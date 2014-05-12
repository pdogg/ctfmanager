from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ctfmanager.views.home', name='home'),
    # url(r'^ctfmanager/', include('ctfmanager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^ctfweb/', include('ctfweb.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('', RedirectView.as_view(url='/ctfweb/scoreboard/')),
)
