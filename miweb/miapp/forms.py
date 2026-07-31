from django import forms
from .models import Tareas
from .models import Pataton
from .models import Comentario

# class CrearNuevaTarea(forms.Form): # Este lo hace de forma manual y hay que ponerle tu que es cada campo (Te damas libertad)
    # titulo = forms.CharField(label="Titulo de la tarea", max_length=200)
    # descripcion = forms.CharField(label="Descripcion de la tarea",widget=forms.Textarea, required=False) 
 
class CrearNuevaTarea(forms.ModelForm): #Este que usa el ModelForm sirve para que django te coja los campos automaticamente del modelo que le pases
    class Meta:
        model = Tareas              
        fields = ['titulo', 'descripcion','prioridad','estado','fecha_limite','tiempo_estimado','usuario','imagen'] 

class EditarTarea(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['titulo', 'descripcion','prioridad','estado','fecha_limite','tiempo_estimado','usuario','imagen'] 
        labels = {
            'titulo': 'Título de la tarea',
            'descripcion': 'Descripción de la tarea',
            'prioridad' : 'Prioridad de la tarea',
            'estado' : 'Estado de la tarea',
            'fecha_limite' : 'Fecha limite de la tarea',
            'tiempo_estimado' : 'Tiempo estimado para esta tarea',
            'usuario' : 'Usuario al que se le asigna la tarea',
            'imagen' : 'Imagen adjunta'
        }


class CrearNuevoPataton(forms.ModelForm): 
    class Meta:
        model = Pataton              
        fields = ['nombre'] 

class EditarPataton(forms.ModelForm):
    class Meta:
        model = Pataton
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre del pataton'
        }

class EditarComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto', 'imagen']