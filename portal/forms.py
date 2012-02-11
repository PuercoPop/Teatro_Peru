
from django import forms
import models

class PuestaEnEscena(forms.Form):
    titulo = forms.CharField()
    plaza = forms.CharField()
    portada = forms.ImageField()
    
class Entrada(forms.ModelForm):
    class Meta:
        model = models.Entrada
    
class Elenco_val(forms.Form):
    nombre = forms.CharField()
    posicion = forms.CharField()
