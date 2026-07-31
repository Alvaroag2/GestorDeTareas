from django.urls import path
from . import views

urlpatterns = [
    path('pataton/',views.pataton,name = 'pataton'),
    path('tareas/',views.tareas, name='tareas'),
    path('hello/<str:user>',views.helloWithParam, name= 'hello'),
    path('crearTareas/',views.crearTareas, name='crearTareas'),
    path('crearPatatones/',views.crearPataton, name='crearPatatones'),
    path('elminarPataton/<int:id>',views.eliminarPataton, name= 'eliminarPataton'),
    path('editarPataton/<int:id>',views.editarPataton, name='editarPataton'),
    path('elminarTarea/<int:id>',views.eliminarTarea, name= 'eliminarTarea'),
    path('realizarTarea/<int:id>',views.realizarTarea, name= 'realizarTarea'),
    path('editarTarea/<int:id>',views.editarTarea, name='editarTarea'),
    path('tareas/buscar/', views.buscarTarea, name='buscarTarea'),
    path('tarea/<int:tarea_id>/', views.detalleTarea, name='detalleTarea'),
    path('elminarComentario/<int:id>',views.eliminarComentario, name= 'eliminarComentario'),
    path('comentario/editar/<int:id>/', views.editarComentario, name='editarComentario'),
    path('tarea/duplicar/<int:tarea_id>/', views.duplicarTarea, name='duplicarTarea'),
    path('tarea/<int:tarea_id>/cronometro/', views.cambiarEstadoCronometro, name='cambiarEstadoCronometro'),

]
