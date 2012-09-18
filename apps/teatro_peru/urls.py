# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

from teatro_peru import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$',
        views.cartelera,
        name="home"),
    url(r'^cartelera/$',
        views.cartelera,
        name="Billboard",),
    url(r'^puesta_en_escena/(?P<puesta_id>\d+)$',
        views.show_showing,
        name="show_showing",
        ),
    url(r'^obra/(?P<play_id>\d+)$',
        views.show_play,
        name="show_play"),
    url(r'^plaza/(?P<plaza>\d+)$',
        views.show_plaza,
        name="show_plaza",),
    url(r'^elenco/(?P<elenco_id>\d+)$', views.elenco_view ),
    url(r'^hoy/$',
        views.billboard_at_date,
        name="billboard_today",
        ),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$',
        views.billboard_at_date,
        name="billboard_at_date",
        ),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$',
        views.billboard_at_date
        ),
    url(r'^(?P<year>\d+)/$', views.billboard_at_date),
    url(r'^crear_puesta/$',
        views.create_showing,
        name="create_showing",
        ),
    url(r'^login/',
        views.log_user,
        {},
        name="login",
        ),
    url(r'^logout/', views.logout_user, {} ),
                       url(r'^create_user/', views.create_user, {}),
    url(r'^buscar/obra/titulo$', views.search_by_title),
    url(r'^validar_entrada/$',
        views.validate_ticket,
        name="validate_ticket",
        ),
    url(r'^validar_elenco/$', views.validate_cast),
    )
