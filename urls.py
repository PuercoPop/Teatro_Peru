# coding=utf8

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

import portal.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Teatro_Peru.views.home', name='home'),
    # url(r'^Teatro_Peru/', include('Teatro_Peru.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
                           url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
                           url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', portal.views.cartelera),
                       url(r'^cartelera/$', portal.views.cartelera),
                       url(r'^cartelera2/$', portal.views.cartelera),
                       url(r'^puesta_en_escena/(?P<puesta_id>\d+)$', portal.views.puesta_view),
                       url(r'^obra/(?P<obra>\d+)$', portal.views.obra_view),
                       url(r'^plaza/(?P<plaza>\d+)$', portal.views.plaza_view),
                       url(r'^elenco/(?P<elenco_id>\d+)$', portal.views.elenco_view ),
                       url(r'^hoy/$', portal.views.cartelera_fecha,),
                       url(r'^(?P<ano>\d+)/(?P<mes>\d+)/(?P<dia>\d+)$', portal.views.cartelera_fecha),
                       url(r'^(?P<ano>\d+)/(?P<mes>\d+)/$', portal.views.cartelera_fecha),
                       url(r'^(?P<ano>\d+)/$', portal.views.cartelera_fecha),
                       url(r'^media/(?P<path>.*)$','django.views.static.serve', { 'document_root':settings.MEDIA_ROOT , 'show_indexes': True } ),
                       url(r'^crear_puesta/$',portal.views.crear_puesta ),
                       #url(r'^static/(?P<path>.*)$','django.views.static.serve', { 'document_root':settings.STATIC_ROOT , 'show_indexes': True } ),
                       #url('', include('social_auth.urls') ),
                       url(r'^la_facebook/', include('la_facebook.urls') ),
                       url(r'^login/', portal.views.log_user, {} ),
                       url(r'^logout/', portal.views.logout_user, {} ),
                       url(r'^create_user/', portal.views.create_user, {}),
                       url(r'^buscar/obra/titulo$', portal.views.buscar_titulo),
                       url(r'^validar_entrada/$', portal.views.validate_entrada ),
                       url(r'^validar_elenco/$', portal.views.validate_cast),
    
    
)
