import json

from django.contrib import messages
import requests
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User


from usuarios.models import Perfil 
from .models import Categoria
from .models import Usuario
from .models import Comentario, Pataton
from .models import Tareas
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.core.files.base import ContentFile
from .forms import CrearNuevaTarea
from .forms import EditarTarea
from .forms import CrearNuevoPataton
from .forms import EditarPataton
from .forms import EditarComentarioForm
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
@ensure_csrf_cookie
def api_categorias(request):
    if request.method == 'GET':
        categorias_qs = Categoria.objects.all()
        data = []
        for cat in categorias_qs:
            data.append({
                "id": cat.id,
                "nombre": cat.nombre,
                "descripcion": cat.descripcion,
            })
        return JsonResponse(data, safe=False, status=200)

    elif request.method == 'POST':
            try:
                body = json.loads(request.body)
                nombre = body.get('nombre')
                descripcion = body.get('descripcion')
    
                
                nueva_categoria = Categoria.objects.create(
                    nombre = nombre,
                    descripcion = descripcion
                )
    
    
                return JsonResponse({
                    "id": nueva_categoria.id,
                    "nombre": nueva_categoria.nombre,
                    "descripcion": nueva_categoria.descripcion
                }, status=201)
            except Exception as e:
                return JsonResponse({"error": "Error al crear la categoria"}, status=400)
    
        

@ensure_csrf_cookie
def api_categoria_detalle(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    # GET /api/categorias/<id>/ -> Obtener categoria por ID
    if request.method == 'GET':
        return JsonResponse({
            "id": categoria.id,
            "nombre": categoria.nombre,
            "descripcion": categoria.descripcion,
        }, status=200)



    elif request.method == 'PUT':
            try:
                body = json.loads(request.body)
                categoria.nombre = body.get('nombre', categoria.nombre)
                categoria.descripcion = body.get('descripcion', categoria.descripcion)
                categoria.save()
    
    
                return JsonResponse({
                    "id": categoria.id,
                    "nombre": categoria.nombre,
                    "descripcion": categoria.descripcion
                }, status=200)
            except Exception as e:
                return JsonResponse({"error": "Error al actualizar el usuario"}, status=400)


    # DELETE /api/categoias/<id>/ -> Borrar categoria
    elif request.method == 'DELETE':
        categoria.delete()
        return HttpResponse(status=204)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

@ensure_csrf_cookie
def api_tareas(request):
    if request.method == 'GET':
        #tareas_qs = Tareas.objects.select_related('usuario', 'categoria').all() #Trae el usuario y la categoria en una sola consulta

        estado_param = request.GET.get('estado')
        prioridad_param = request.GET.get('prioridad')
        categoria_param = request.GET.get('categoria') or request.GET.get('categoria_id')
        usuario_param = request.GET.get('usuario') or request.GET.get('usuario_id')

        
        MAPA_ESTADOS = {'pendiente': 'PEN', 'en proceso': 'PRO', 'completada': 'COM'}
        MAPA_PRIORIDADES = {'baja': 'B', 'media': 'M', 'alta': 'A'}

        
        filtros = {}

        if estado_param:
            
            estado_val = MAPA_ESTADOS.get(estado_param.lower(), estado_param) #Busca el parametro en el mapa y te lo devuelve, sino te da el valor por defecto
            filtros['estado'] = estado_val #Busca el estado en la base de datos

        if prioridad_param:
            
            prioridad_val = MAPA_PRIORIDADES.get(prioridad_param.lower(), prioridad_param)
            filtros['prioridad'] = prioridad_val

        if categoria_param:
            filtros['categoria_id'] = categoria_param

        if usuario_param:
            filtros['usuario_id'] = usuario_param

        
        tareas_qs = Tareas.objects.filter(**filtros).select_related('categoria', 'usuario') #En Python poner ** delante de un diccionario al pasarlo a una función significa "desempaquetar el diccionario como argumentos".

        data = []
        for tar in tareas_qs:
            data.append({
                "id": tar.id,
                "titulo": tar.titulo,
                "descripcion": tar.descripcion,
                "estado": tar.get_estado_display().lower(),  # Convierte 'PEN' -> 'pendiente'
                "prioridad": tar.get_prioridad_display().lower(),  # Convierte 'A' -> 'alta'
                "fecha_creacion": tar.fecha_creacion.strftime('%Y-%m-%d'),
                "fecha_limite": tar.fecha_limite.strftime('%Y-%m-%d') if tar.fecha_limite else None,
                "usuario": {
                    "id": tar.usuario.id,
                    "nombre": tar.usuario.first_name or tar.usuario.username
                },
                "categoria": {
                    "id": tar.categoria.id,
                    "nombre": tar.categoria.nombre
                } if hasattr(tar, 'categoria') and tar.categoria else None
            })
        return JsonResponse(data, safe=False, status=200)
    

    elif request.method == 'POST':
            try:
                body = json.loads(request.body)
                titulo = body.get('titulo')
                descripcion = body.get('descripcion')
                estado = body.get('estado', 'PEN')
                prioridad = body.get('prioridad', 'M')
                fecha_limite = body.get('fecha_limite')
                categoria_id = body.get('categoria_id')
                usuario_id = body.get('usuario_id')
    
                
                nueva_tarea = Tareas.objects.create(
                    titulo = titulo,
                    descripcion = descripcion,
                    estado = estado,
                    prioridad = prioridad,
                    fecha_limite = fecha_limite,
                    categoria_id = categoria_id,
                    usuario_id = usuario_id
                )
    
                
    
                return JsonResponse({
                    "id": nueva_tarea.id,
                    "titulo": nueva_tarea.titulo,
                    "descripcion": nueva_tarea.descripcion,
                    "estado": nueva_tarea.estado,
                    "prioridad": nueva_tarea.prioridad,
                    "fecha_creacion": nueva_tarea.fecha_creacion.strftime('%Y-%m-%d'),
                    "fecha_limite": nueva_tarea.fecha_limite,
                    "categoria": {
                        "id": nueva_tarea.categoria.id,
                        "nombre": nueva_tarea.categoria.nombre
                    },
                    "usuario": {
                        "id": nueva_tarea.usuario.id,
                        "nombre": nueva_tarea.usuario.first_name or nueva_tarea.usuario.username
                    }
                }, status=201)
            except Exception as e:
                
                print("❌ ERROR EN POST /api/tareas/:", str(e))
                return JsonResponse({"error": str(e)}, status=400)
            
    
        #return JsonResponse({"error": "Método no permitido"}, status=405)

@ensure_csrf_cookie
def api_tareas_detalle(request, id):
    tarea = get_object_or_404(Tareas, id=id)
    if request.method == 'GET':
        

        
        
            return JsonResponse({
                "id": tarea.id,
                "titulo": tarea.titulo,
                "descripcion": tarea.descripcion,
                "estado": tarea.get_estado_display().lower(),  # Convierte 'PEN' -> 'pendiente'
                "prioridad": tarea.get_prioridad_display().lower(),  # Convierte 'A' -> 'alta'
                "fecha_creacion": tarea.fecha_creacion.strftime('%Y-%m-%d'),
                "fecha_limite": tarea.fecha_limite.strftime('%Y-%m-%d') if tarea.fecha_limite else None,
                "usuario": {
                    "id": tarea.usuario.id,
                    "nombre": tarea.usuario.first_name or tarea.usuario.username
                },
                "categoria": {
                    "id": tarea.categoria.id,
                    "nombre": tarea.categoria.nombre
                } if hasattr(tarea, 'categoria') and tarea.categoria else None
            })


    elif request.method == 'PUT':
            try:
                body = json.loads(request.body)
                tarea.titulo = body.get('titulo', tarea.titulo)
                tarea.descripcion = body.get('descripcion', tarea.descripcion)
                tarea.estado = body.get('estado', tarea.estado)
                tarea.prioridad = body.get('prioridad', tarea.prioridad)
                tarea.fecha_limite = body.get('fecha_limite', tarea.fecha_limite)
                cat_id = body.get('categoria_id')
                if cat_id is not None:
                    tarea.categoria = Categoria.objects.get(id=cat_id)
                usr_id = body.get('usuario_id')
                if usr_id is not None:
                    tarea.usuario = User.objects.get(id=usr_id)
                tarea.save()
    
                
    
                return JsonResponse({
                    "id": tarea.id,
                    "titulo": tarea.titulo,
                    "descripcion": tarea.descripcion,
                    "estado": tarea.get_estado_display().lower(),  # Convierte 'PEN' -> 'pendiente'
                    "prioridad": tarea.get_prioridad_display().lower(),  # Convierte 'A' -> 'alta'
                    "fecha_creacion": tarea.fecha_creacion.strftime('%Y-%m-%d'),
                    "fecha_limite": tarea.fecha_limite.strftime('%Y-%m-%d') if tarea.fecha_limite else None,
                    "usuario": {
                        "id": tarea.usuario.id,
                        "nombre": tarea.usuario.first_name or tarea.usuario.username
                    },
                    "categoria": {
                        "id": tarea.categoria.id,
                        "nombre": tarea.categoria.nombre
                    } if hasattr(tarea, 'categoria') and tarea.categoria else None
                    
                }, status=200)
            except Exception as e:
                return JsonResponse({"error": "Error al actualizar la tarea"}, status=400)
    
    elif request.method == 'DELETE':
            tarea.delete()
            return HttpResponse(status=204)
        
    return JsonResponse({"error": "Método no permitido"}, status=405)
        
    
def api_mistareas(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "No has iniciado sesión"}, status=401)
    

    tareas = Tareas.objects.filter(usuario=request.user).select_related('categoria', 'usuario')
        

        
    
    lista_tareas = []
    for tarea in tareas:
        lista_tareas.append({
            "id": tarea.id,
            "titulo": tarea.titulo,
            "descripcion": tarea.descripcion,
            "estado": tarea.get_estado_display().lower(),
            "prioridad": tarea.get_prioridad_display().lower(),
            "fecha_creacion": tarea.fecha_creacion.strftime('%Y-%m-%d'),
            "fecha_limite": str(tarea.fecha_limite) if tarea.fecha_limite else None,
            "usuario": {
                "id": tarea.usuario.id,
                "nombre": tarea.usuario.first_name or tarea.usuario.username
            },
            "categoria": {
                "id": tarea.categoria.id,
                "nombre": tarea.categoria.nombre
            } if tarea.categoria else None
        })

        #safe=False permite listas en JsonResponse(Es obligatorio)
        return JsonResponse(lista_tareas, safe=False, status=200) 


def comprobarfestivo(request, id):
    tarea = get_object_or_404(Tareas, id=id)
    if not tarea.fecha_limite:
        return JsonResponse({
            "es_festivo": False,
            "festivo": None,
            "mensaje": "La tarea no tiene fecha límite asignada"
        }, status=200)
    fecha_str = str(tarea.fecha_limite)  
    año = fecha_str.split('-')[0]
    url = f"https://date.nager.at/api/v3/PublicHolidays/{año}/ES"

    try:
        
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            festivos = response.json()

            
            for festivo in festivos:
                if festivo['date'] == fecha_str:
                    return JsonResponse({
                        "es_festivo": True,
                        "festivo": festivo['localName']
                    }, status=200)

        # Si finaliza el bucle y no hubo coincidencias
        return JsonResponse({
            "es_festivo": False,
            "festivo": None
        }, status=200)

    except requests.RequestException:
        
        return JsonResponse({
            "error": "No se pudo consultar el servicio externo de festivos"
        }, status=503)