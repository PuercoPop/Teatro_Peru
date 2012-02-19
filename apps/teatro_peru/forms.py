
from django.forms import ModelForm, CharField, EmailField, PasswordInput
from models import PuestaEnEscena, Entrada, Obra, Plaza, Review, \
        Article, CastMember, UserProfile

from teatro_peru import strings

class PuestaEnEscenaForm(ModelForm):
    class Meta:
        model = PuestaEnEscena
    
class EntradaForm(ModelForm):
    class Meta:
        model = Entrada
    
class CastMemberForm(ModelForm):
    class Meta:
        model = CastMember

class UserProfileForm(ModelForm):
    username = CharField( label=strings.USERNAME)
    password = CharField( widget=PasswordInput, label = strings.PASSWORD )
    email = EmailField( label=strings.EMAIL )
    first_name = CharField( required=False, label=strings.FIRST_NAME )
    last_name = CharField( required=False, label=strings.LAST_NAME )

    class Meta:
        model = UserProfile
        fields = ('username', 'profile_picture', 'password', 'email', \
                 'hideEmail', 'first_name', 'last_name' )
        exclude = ('is_staff', 'is_active', 'is_superuser', 'date_joined',\
                'last_login', 'groups','user_permissions', 'user' )
