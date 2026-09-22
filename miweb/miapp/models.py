from django.utils import timezone

from django.db import models
from usuarios.models import Usuario
from django.contrib.auth.models import User

# Create your models here.
class Pataton(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Tareas(models.Model):
    PRIORIDAD_CHOICES = [
        ('B', 'Baja'),    
        ('M', 'Media'),   
        ('A', 'Alta'),    
    ]
    
    ESTADO_CHOICES = [
        ('PEN', 'Pendiente'),
        ('PRO', 'En Proceso'),
        ('COM', 'Completada'),
    ]
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    realizada = models.BooleanField(default=False)
    prioridad = models.CharField(max_length=1, choices=PRIORIDAD_CHOICES, default='M')
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default='PEN')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField(null=True, blank=True)
    tiempo_estimado = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.0, 
        help_text="Tiempo estimado en horas (ej. 2.5)"
    )
    tiempo_trabajado = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.0, 
        help_text="Tiempo real trabajado en horas (ej. 1.0)"
    )
    inicio_trabajo = models.DateTimeField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) #El on_delete on cascade hace que si se borra algo que tiene relacion se borre aqui tambien
    imagen = models.ImageField(upload_to='tareas_imagenes/', null=True, blank=True)

    categoria = models.ForeignKey(
        'Categoria', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tareas'
    )


    @property
    def esta_vencida(self):
        """Devuelve True si tiene fecha límite, no está realizada y la fecha es anterior a hoy"""
        if self.fecha_limite and not self.realizada:
            return self.fecha_limite < timezone.now().date()
        return False

    def tiempo_restante(self):
        restante = self.tiempo_estimado - self.tiempo_trabajado
        return max(restante, 0)

    # def __str__(self):
        # return self.titulo + "-" + self.descripcion + "-" + self.prioridad + "-" + self.estado + "-" + self.fecha_creacion + "-" + self.fecha_limite
    
    def __str__(self):
        creacion = self.fecha_creacion.strftime('%d/%m/%Y')
        limite = self.fecha_limite.strftime('%d/%m/%Y') if self.fecha_limite else "Sin fecha límite"
        return f"{self.titulo} - Creada: {creacion} - Límite: {limite}"
    


class Comentario(models.Model):
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='tareas_imagenes/', null=True, blank=True)
    tarea = models.ForeignKey(Tareas, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Comentario de" + self.usuario.username + "en" + self.tarea.titulo


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre    