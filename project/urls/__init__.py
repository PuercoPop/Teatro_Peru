# -*- coding:utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                url(r'^admin/', include(admin.site.urls)),

                url(r'^', include('teatro_peru.urls')),
                #url('', include('social_auth.urls') ),
                url(r'^la_facebook/', include('la_facebook.urls') ),
)

if settings.DEBUG == True:
    from os.path import join
    from django.conf.urls.static import static
    from django.views.static import serve
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$',
                serve, {
                    'document_root':settings.STATIC_ROOT,
                    'show_indexes': True
                    }),
            url(r'^media/(?P<path>.*)$',
                serve, {
                    'document_root':settings.MEDIA_ROOT,
                    'show_indexes': True
                    }),
                )
