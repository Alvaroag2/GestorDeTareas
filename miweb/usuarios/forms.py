from django import forms
from .models import Usuario


class CrearNuevoUsuario(forms.ModelForm): #Este que usa el ModelForm sirve para que django te coja los campos automaticamente del modelo que le pases
    class Meta:
        model = Usuario              
        fields = ['correo','contraseña'] 

class EditarUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['correo','contraseña']
        labels = {
            'correo': 'Correo electronico',
            'contraseña': 'Contraseña para tu cuenta',
        }