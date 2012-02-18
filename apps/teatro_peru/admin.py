# coding=utf8

from django.contrib import admin
from teatro_peru.models import Horario,Entrada, Obra, Plaza, PuestaEnEscena, CastMember, Rating, Review, AVField

admin.site.register(Horario)
admin.site.register(Entrada)
admin.site.register(Plaza)
admin.site.register(Obra)
admin.site.register(PuestaEnEscena)
admin.site.register(CastMember)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(AVField)
