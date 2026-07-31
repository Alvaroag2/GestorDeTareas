from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/',views.usuarios,name = 'usuarios'),
    path('crearUsuarios/',views.crearUsuarios, name='crearUsuarios'),
    path('elminarUsuario/<int:id>',views.eliminarUsuario, name= 'eliminarUsuario'),
    path('editarUsuario/<int:id>',views.editarUsuario, name='editarUsuario'),
    path('login',views.login, name= 'login'),
    path('logout',views.logout, name= 'logout'),
]