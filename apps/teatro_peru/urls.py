# coding=utf8

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from teatro_peru import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.cartelera),
                       url(r'^cartelera/$', views.cartelera),
                       url(r'^puesta_en_escena/(?P<puesta_id>\d+)$', views.puesta_view),
                       url(r'^obra/(?P<obra>\d+)$', views.obra_view),
                       url(r'^plaza/(?P<plaza>\d+)$', views.plaza_view),
                       url(r'^elenco/(?P<elenco_id>\d+)$', views.elenco_view ),
                       url(r'^hoy/$', views.cartelera_fecha,),
                       url(r'^(?P<ano>\d+)/(?P<mes>\d+)/(?P<dia>\d+)$', views.cartelera_fecha),
                       url(r'^(?P<ano>\d+)/(?P<mes>\d+)/$', views.cartelera_fecha),
                       url(r'^(?P<ano>\d+)/$', views.cartelera_fecha),
                       url(r'^crear_puesta/$',views.crear_puesta ),
                       url(r'^login/', views.log_user, {} ),
                       url(r'^logout/', views.logout_user, {} ),
                       url(r'^create_user/', views.create_user, {}),
                       url(r'^buscar/obra/titulo$', views.buscar_titulo),
                       url(r'^validar_entrada/$', views.validate_entrada ),
                       url(r'^validar_elenco/$', views.validate_cast),
    
    
)
