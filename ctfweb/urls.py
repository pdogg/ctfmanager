from django.conf.urls import patterns, url
from django.contrib.auth.views  import *
from django.views.generic.base import RedirectView, TemplateView

from ctfweb import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
        url(r'^challenges/', views.allchallenges, name='challenges'),
	url(r'^scoreboard/', views.scoreboard, name='scoreboard'),
	url(r'^challenge/(?P<challenge_id>\d+)/$', views.challenge, name='challenge'),
	url(r'^submitkey/(?P<challenge_id>\d+)/$', views.submitkey, name='submitkey'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'ctfweb/login.html'}),
	url(r'^logout/', views.logout_view, name='logout'),
	url(r'^register/$', views.registerform, name='registerform'),
	url(r'^registerprocess/$', views.registerprocess, name='registerprocess'),
	url(r'^rules/', TemplateView.as_view(template_name='ctfweb/rules.html')),
	url(r'^competitor/(?P<comp_id>\d+)/$', views.competitordetail, name='competitor'),
)


