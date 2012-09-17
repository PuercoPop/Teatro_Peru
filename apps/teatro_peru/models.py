# -*- coding:utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from teatro_peru import strings

class Schedule(models.Model):
    DAY_CHOICES = (
            (u'L', u'Lunes'),
            (u'M', u'Martes'),
            (u'X', u'Miércoles'),
            (u'J', u'Jueves'),
            (u'V', u'Viernes'),
            (u'S', 'Sábado'),
            (u'D', 'Domingo')
            )
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)

    def __unicode__(self):
        return u'%s: %s' % (self.day, self.start_time)


class Ticket(models.Model):
    """
    Model for a ticket, name and cost in soles.
    """
    name = models.CharField(max_length=30)
    cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return u'%s: %d' % (self.name, self.cost)


class Theatre(models.Model):
    """
    Theatre where the play is showing. Link to google maps/foursquare?
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    map_link = models.URLField(verify_exists=True, max_length=100, blank=True)
    perfil = models.ForeignKey('AVField', blank=True)

    def __unicode__(self):
        return u'%s' % (self.name,)


class Play(models.Model):
    """
    Play information.
    """
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    #Date of publishing
    date = models.DateField(blank=True)
    origin_language = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    #related

    def __unicode__(self):
        return u'%s de %s' % ( self.title, self.author )


class Rating(models.Model):
    """
    Generic model to rate another model.
    """
    like = models.PositiveIntegerField( default = 0 )
    dislike = models.IntegerField( default = 0 )

    def __unicode__(self):
        return u'Likes: %d, Dislikes: %d' % (self.like, self.dislike)


class Review(models.Model):
    """
    Review of a Showing
    """
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=24)
    text = models.CharField(max_length=1500)
    date = models.DateField(auto_now_add=True)
    rating = models.OneToOneField('Rating')
    #Optional para las External
    url = models.URLField(verify_exists=True, blank=True, null=True)

    def __unicode__(self):
        return u'Reseña por %s' % (self.author)


class Showing(models.Model):
    """
    The 'instance' of a play
    """
    theatre = models.ForeignKey('Theatre')
    play = models.ForeignKey('Play')
    season_start = models.DateField()
    season_end = models.DateField()
    ticket = models.ManyToManyField('Ticket')
    schedule = models.ManyToManyField('Schedule')
    rating = models.OneToOneField('Rating')
    sumilla = models.CharField(max_length=1000, blank=True)
    reviews = models.ManyToManyField(Review, blank=True)
    interviews = models.ManyToManyField('Article', blank=True, null=True)
    cast = models.ManyToManyField('CastMember', blank=True)
    profile = models.ForeignKey('AVField',
            blank=True,
            null=True,
            related_name = 'Showing_profile',
            )
    media = models.ManyToManyField('AVField',
            blank=True,
            null=True,
            related_name = 'Showing_media',
            )

    def __unicode__(self):
        return u'%s en %s' % ( self.obra.title, self.theatre.name )


class Article(models.Model):
    """
    For interviews and coverage of plays
    """
    author = models.CharField(max_length=30)
    text = models.CharField(max_length = 5000)
    date = models.DateField(auto_now_add=True)
    rating = models.OneToOneField('Rating')

    def __unicode__(self):
        return u'%s, %s en %s' % (self.author, self.text, self.date)


class CastMember(models.Model):
    """
    Cast member model, may be related to a user profile, display workphone, etc
    """
    name = models.CharField(max_length=100)
    lastname  = models.CharField(max_length=100)
    email = models.EmailField(max_length=75,
            blank = True,
            verbose_name = u'Correo Eléctronico',
            )
    telephone = models.IntegerField(blank=True, null=True,)
    cellphone = models.IntegerField( blank=True,
            null=True,
            verbose_name = u'Celular',
            )
    reviews = models.ManyToManyField('Review', blank=True)
    role = models.CharField( max_length = 30)
    rating = models.OneToOneField('Rating')
    profile = models.ForeignKey('AVField',
            blank=True,
            null=True,
            related_name = 'CastMember_profile'
            )
    media = models.ManyToManyField(
        'AVField',
        blank=True,
        null=True,
        related_name = 'CastMember_media',
        )

    def __unicode__(self):
        return u'%s: %s %s' % (self.role, self.name, self.lastname)


class AVField(models.Model):
    """
    A Video or Image
    """
    FILE_TYPE_CHOICES = (
            (u'IMG', u'Imagen'),
            (u'VID', u'Video'),
            )
    path = models.FileField(upload_to='uploaded_media/')
    f_type = models.CharField( max_length = 10, choices = FILE_TYPE_CHOICES)
    uploaded_by = models.ForeignKey('UserProfile')

    def __unicode__(self):
        return u'%s: %s' % ( self.filename, self.f_type )


class UserProfile(User):
    """
    User Profile
    """
    user = models.OneToOneField(User)
    #other_fields here
    profile_picture = models.ImageField(upload_to= 'Profile_Pictures',
            verbose_name=strings.PROFILE_PICTURE, blank=True)
    hideEmail = models.BooleanField(verbose_name=strings.HIDE_EMAIL,
            blank=True)

    def __unicode__(self):
        return u'%s' % (self.user,)
