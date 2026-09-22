from django.urls import path
from . import views

urlpatterns = [
    path('api/csrf/', views.api_csrf, name='api_csrf'),
        path('api/login/', views.api_login, name='api_login'),
        path('api/sesion/', views.api_sesion, name='api_sesion'),
        path('api/logout/', views.api_logout, name='api_logout'),
    
        
        path('api/usuarios/', views.api_usuarios, name='api_usuarios'),
        path('api/usuarios/<int:id>/', views.api_usuario_detalle, name='api_usuario_detalle'),
]