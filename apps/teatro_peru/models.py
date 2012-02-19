# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from teatro_peru import strings

class Horario(models.Model):
    DAY_CHOICES = ( 
            (u'L', u'Lunes'),
            (u'M', u'Martes'),
            (u'X', u'Miércoles'),
            (u'J', u'Jueves'),
            (u'V', u'Viernes'),
            (u'S', 'Sábado'),
            (u'D', 'Domingo')
            )
    day = models.CharField( max_length=10, choices=DAY_CHOICES )
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True,null=True)
    
    def __unicode__(self):
        return u'%s: %s' % ( self.day, self.start_time )

class Entrada(models.Model):
  name = models.CharField(max_length=30)
  cost = models.DecimalField( max_digits=6, decimal_places=2)# MaxValue:9999.99
  
  def __unicode__(self):
      return u'%s: %d' % ( self.name, self.cost)

class Plaza(models.Model):
  nombre = models.CharField(max_length = 100)
  direccion = models.CharField(max_length = 100)
  map_link = models.URLField( verify_exists=True, max_length=100, blank=True )
  
  def __unicode__(self):
      return u'%s' % ( self.nombre, )
      
class Obra(models.Model):
  titulo = models.CharField( max_length = 100 )
  autor = models.CharField( max_length = 100)
  fecha = models.DateField( blank=True )      
  idioma_orignal = models.CharField( max_length = 100, blank=True )
  pais = models.CharField( max_length = 100, blank=True )
  
  def __unicode__(self):
      return u'%s de %s' % ( self.titulo, self.autor )


class Rating(models.Model):
    like = models.PositiveIntegerField( default = 0 )
    dislike = models.IntegerField( default = 0 )

    def __unicode__(self):
        return u'Likes: %d, Dislikes: %d' % (self.like,self.dislike)

class Review(models.Model):
    """
    Reseña
    """
    autor = models.CharField( max_length = 30 )
    titulo = models.CharField( max_length = 24)
    text = models.CharField( max_length = 1500 )
    fecha = models.DateField( auto_now_add = True )
    rating = models.OneToOneField('Rating')
    #Optional para las External
    url = models.URLField( verify_exists=True, blank=True, null=True )
    
    def __unicode__(self):
        return u'Reseña por %s' % ( self.autor )

class PuestaEnEscena(models.Model):
  plaza = models.ForeignKey('Plaza')
  obra = models.ForeignKey('Obra')
  inicio_de_temporada = models.DateField()
  fin_de_temporada = models.DateField()
  entradas = models.ManyToManyField('Entrada')
  horarios = models.ManyToManyField('Horario')
  rating = models.OneToOneField('Rating')
  sumilla = models.CharField( max_length = 1000, blank=True )
  reviews = models.ManyToManyField(Review, blank=True )
  entrevistas = models.ManyToManyField('Article', blank=True,null=True)
  elenco = models.ManyToManyField('CastMember', blank=True )
  perfil = models.ForeignKey('AVField', blank=True, null=True, related_name = 'PuestaEnEscena_perfil' )
  media = models.ManyToManyField('AVField', blank=True, null=True, related_name = 'PuestaEnEscena_media' )
  
  def __unicode__(self):
      return u'%s en %s' % ( self.obra.titulo, self.plaza.nombre )


class Article(models.Model):
    """
    Para Entrevistas
    """
    autor = models.CharField( max_length = 30)
    text = models.CharField( max_length = 5000 )
    fecha = models.DateField( auto_now_add = True )
    rating = models.OneToOneField('Rating')

    
        
class CastMember(models.Model):
  nombre = models.CharField( max_length = 100 )
  apellido = models.CharField( max_length = 100)
  email = models.EmailField( max_length=75, blank = True, verbose_name = u'Correo Eléctronico' )
  telefono = models.IntegerField( blank=True, null=True )
  movil = models.IntegerField( blank=True, null=True, verbose_name = u'Celular' )
  reviews = models.ManyToManyField('Review', blank=True)
  role = models.CharField( max_length = 30)
  rating = models.OneToOneField('Rating')
  perfil = models.ForeignKey('AVField', blank=True, null=True, related_name = 'CastMember_perfil' )
  media = models.ManyToManyField('AVField', blank=True, null=True, related_name = 'CastMember_media' )
  
  def __unicode__(self):
      return u'%s: %s %s' % (self.role, self.nombre, self.apellido)

class Plaza(models.Model):
  nombre = models.CharField(max_length = 100)
  direccion = models.CharField(max_length = 100)
  map_link = models.URLField( verify_exists=True, max_length=100 )
  perfil = models.ForeignKey('AVField', blank=True)
  
  def __unicode__(self):
      return u'%s: %s' % ( self.nombre, self.direccion )

  
  
class AVField(models.Model):
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
    user = models.OneToOneField(User)
    #other_fields here
    profile_picture = models.ImageField(upload_to= 'Profile_Pictures',\
            verbose_name=strings.PROFILE_PICTURE, blank=True)
    hideEmail = models.BooleanField(verbose_name=strings.HIDE_EMAIL, blank=True)
    
    def __unicode__(self):
        return u'%s' % (self.user,)
