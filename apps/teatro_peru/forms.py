# -*- coding: utf-8 -*-

from django import forms
from .models import Play, Ticket, CastMember, UserProfile
import .strings


class PlayForm(forms.ModelForm):
    class Meta:
        model = Play

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket

class CastMemberForm(forms.ModelForm):
    class Meta:
        model = CastMember

