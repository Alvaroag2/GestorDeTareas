from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Usuario(models.Model):
    correo = models.EmailField(unique=True) # unique=True evita correos duplicados
    contraseña = models.CharField(max_length=50) 
    def __str__(self):
        return self.correo


class Perfil(models.Model):
    
    class Rol(models.TextChoices):
        USUARIO_COMUN = 'COMUN', 'Usuario Comun'
        JEFE_EQUIPO = 'JEFE', 'Jefe de Equipo'
        ADMINISTRADOR = 'ADMIN', 'Administrador'

    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    
    rol = models.CharField(
        max_length=10,
        choices=Rol.choices,
        default=Rol.USUARIO_COMUN,
    )

    def __str__(self):
        return self.usuario.username + "-" + self.get_rol_display()