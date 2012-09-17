# -*- coding: utf-8 -*-

from django import forms
import .strings


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(label=strings.USERNAME,)
    password = forms.CharField(
        widget=PasswordInput,
        label=strings.PASSWORD,)
    email = forms.EmailField(
        label=strings.EMAIL,)
    first_name = forms.CharField(
        required=False,
        label=strings.FIRST_NAME,)
    last_name = forms.CharField(
        required=False,
        label=strings.LAST_NAME,)

    class Meta:
        model = UserProfile
        fields = ('username',
                  'profile_picture',
                  'password',
                  'email',
                  'hideEmail',
                  'first_name',
                  'last_name',)
        exclude = ('is_staff',
                   'is_active',
                   'is_superuser',
                   'date_joined',
                   'last_login',
                   'groups',
                   'user_permissions',
                   'user',)
