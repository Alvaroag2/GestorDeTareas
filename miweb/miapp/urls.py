from django.urls import path
from . import views

urlpatterns = [
    path('api/tareas/', views.api_tareas, name='api_tareas'),
    path('api/tareas/<int:id>/', views.api_tareas_detalle, name='api_tareas_detalle'),
    path('api/mistareas/', views.api_mistareas, name='api_mistareas'),
    path('api/tareas/<int:id>/comprobarfestivo/', views.comprobarfestivo, name='comprobarfestivo'),
    path('api/categorias/', views.api_categorias, name='api_categorias'),
    path('api/categorias/<int:id>/', views.api_categoria_detalle, name='api_categoria_detalle'),
    

]
