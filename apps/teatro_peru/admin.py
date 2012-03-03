# -*- coding:utf8 -*-

from django.contrib import admin
from teatro_peru.models import Schedule,Ticket, Play, Theatre, Showing, \
        CastMember, Rating, Review, AVField

admin.site.register(Schedule)
admin.site.register(Ticket)
admin.site.register(Theatre)
admin.site.register(Play)
admin.site.register(Showing)
admin.site.register(CastMember)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(AVField)
