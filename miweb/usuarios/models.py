from django.db import models

# Create your models here.
class Usuario(models.Model):
    correo = models.EmailField(unique=True) # unique=True evita correos duplicados
    contraseña = models.CharField(max_length=50) 
    def __str__(self):
        return self.correo
        