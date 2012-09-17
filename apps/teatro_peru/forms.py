# -*- coding: utf-8 -*-

from django import forms
from accounts.models import UserProfile
from teatro_peru.models import Play, Ticket, CastMember
from teatro_peru import strings


class PlayForm(forms.ModelForm):
    class Meta:
        model = Play

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket

class CastMemberForm(forms.ModelForm):
    class Meta:
        model = CastMember

