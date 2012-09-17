# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db.models.signal import post_save

import .strings

class UserProfile(User):
    """
    User Profile
    """
    user = models.OneToOneField(User)
    profile_picture = models.ImageField(
        upload_to= 'Profile_Pictures',
        verbose_name=strings.PROFILE_PICTURE,
        blank=True,)
    hideEmail = models.BooleanField(
        verbose_name=strings.HIDE_EMAIL,
        blank=True,)

    def __unicode__(self):
        return u'%s' % (self.user,)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create, sender=User)
