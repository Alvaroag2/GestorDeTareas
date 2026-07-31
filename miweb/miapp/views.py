from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User

from usuarios.models import Perfil
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

# Create your views here.
def hello(request):
    titulo = "Jamsala Jamsal"
    username = "AG2"
    return render(request,'index.html',{
        "titulo" : titulo,
        "username" : username
    })

def helloWithParam(request,user):
    return HttpResponse("<h1>Hello %s<h1>" %user)

#def pataton(request):
#    pataton = list(Pataton.objects.values())
#    return JsonResponse(pataton, safe=False)

#pataton sin Json
def pataton(request):
   pataton = Pataton.objects.all()
   return render(request,'pataton.html',{
       "pataton" : pataton
   })

# def tareas(request,id):
    #tareas = Tareas.objects.get(id=id)
    # tareas = get_object_or_404(Tareas,id = id)
    # return HttpResponse("<h1>El titulo de tu tarea es %s<h1>" %tareas.titulo)

# def tareas(request): # SIn filtrar por usuairo
    #tareas = Tareas.objects.get(id=id)
    # tareas = Tareas.objects.all()
    # return render(request,'tareas.html',{
    #    "tareas" : tareas
    # })

# def tareas(request):
    #Comprobamos si hay un usuario logueado en la sesión
    # usuario_id = request.session.get('usuario_id')
# 
    # 
    # if not usuario_id:
        # return redirect('login')
# 
    # 
    # mis_tareas = Tareas.objects.filter(usuario_id=usuario_id)
# 
    # 
    # return render(request, 'tareas.html', {
        # 'tareas': mis_tareas
    # })

@login_required  #Si no está logueado django lo manda al login automaticamente que la direccion del login esta definida en settings
def tareas(request):
    es_admin = request.user.perfil.rol == Perfil.Rol.ADMINISTRADOR
    es_jefe = request.user.perfil.rol == Perfil.Rol.JEFE_EQUIPO

    
    if es_admin or es_jefe or request.user.is_superuser:
        lista_tareas = Tareas.objects.all()
    else:
        
        lista_tareas = Tareas.objects.filter(usuario=request.user)

    return render(request, 'tareas.html', {
        'tareas': lista_tareas
    })


# def crearTareas(request): #Este es usando model.Forms haciendo manual
    # if request.method == 'POST':
        # Tareas.objects.create(titulo = request.POST["titulo"],descripcion = request.POST["descripcion"], pataton_id=1)
        # return redirect('crearTareas')
    # return render(request,'crearTareas.html',{
        # "form" : CrearNuevaTarea()
    # }) 

# CON ModelForm (model = Tareas):
# def crearTareas(request):
    # if request.method == 'POST':
        # form = CrearNuevaTarea(request.POST,request.FILES)
        # if form.is_valid():
            # tarea = form.save() 
            # return redirect('tareas') 
    # else:
        # form = CrearNuevaTarea() #Lo crea vacio
# 
    # 
    # return render(request, 'crearTareas.html', {
        # 'form': form
    # })

@login_required
def crearTareas(request):

    es_admin = request.user.perfil.rol == Perfil.Rol.ADMINISTRADOR
    es_jefe = request.user.perfil.rol == Perfil.Rol.JEFE_EQUIPO
    
    if not (es_admin or es_jefe or request.user.is_superuser):
        messages.error(request, "No tienes permisos para crear usuarios.")
        return redirect('usuarios')  

    if request.method == 'POST':
        form = CrearNuevaTarea(request.POST, request.FILES)
        if form.is_valid():
            tarea = form.save()
            return redirect('tareas')
    else:
        form = CrearNuevaTarea()

    return render(request, 'crearTareas.html', {
        'form': form
    })


@login_required
def eliminarTarea(request, id):
    tarea = get_object_or_404(Tareas, id=id, usuario=request.user)
    tarea.delete()
    return redirect('tareas')

# @login_required
# def realizarTarea(request,id):
    # tarea=get_object_or_404(Tareas,id=id)
    # tarea.realizada = True
    # tarea.save()
    # return redirect('tareas')

@login_required
def editarTarea(request, id):

    es_admin = request.user.perfil.rol == Perfil.Rol.ADMINISTRADOR
    es_jefe = request.user.perfil.rol == Perfil.Rol.JEFE_EQUIPO
    
    if not (es_admin or es_jefe or request.user.is_superuser):
        messages.error(request, "No tienes permisos para crear usuarios.")
        return redirect('usuarios')  

    tarea = get_object_or_404(Tareas, id=id)

    if request.method == 'POST':
        
        form = EditarTarea(request.POST, request.FILES , instance=tarea, )
        if form.is_valid():
            form.save() 
            return redirect('tareas')
    else:
        # Petición GET: le pasamos 'instance=tarea' para que cargue los datos actuales
        form = EditarTarea(instance=tarea)

    return render(request, 'editarTarea.html', {
        'form': form,
        'tarea': tarea
    })

# def buscarTarea(request):
    # usuario_id = request.session.get('usuario_id')
    # if not usuario_id:
        # return redirect('login')
# 
    # 
    # busqueda = request.GET.get('q', '')
    # prioridad_filtro = request.GET.get('prioridad', '')  
    # estado_filtro = request.GET.get('estado', '')        
# 
#    
    # mis_tareas = Tareas.objects.filter(usuario_id=usuario_id)
# 
#    
    # if busqueda:
        # mis_tareas = mis_tareas.filter(titulo__icontains=busqueda)
        # 
    # if prioridad_filtro:                                  
        # mis_tareas = mis_tareas.filter(prioridad=prioridad_filtro)
        # 
    # if estado_filtro:                                     
        # mis_tareas = mis_tareas.filter(estado=estado_filtro)
# 
    # 
    # return render(request, 'tareas.html', {
        # 'tareas': mis_tareas,
        # 'busqueda': busqueda,
        # 'prioridad_filtro': prioridad_filtro,             
        # 'estado_filtro': estado_filtro,                   
    # })

@login_required
def buscarTarea(request):
    busqueda = request.GET.get('q', '')
    prioridad_filtro = request.GET.get('prioridad', '')
    estado_filtro = request.GET.get('estado', '')

    
    mis_tareas = Tareas.objects.filter(usuario=request.user)

    if busqueda:
        mis_tareas = mis_tareas.filter(titulo__icontains=busqueda)
        
    if prioridad_filtro:
        mis_tareas = mis_tareas.filter(prioridad=prioridad_filtro)
        
    if estado_filtro:
        mis_tareas = mis_tareas.filter(estado=estado_filtro)

    return render(request, 'tareas.html', {
        'tareas': mis_tareas,
        'busqueda': busqueda,
        'prioridad_filtro': prioridad_filtro,
        'estado_filtro': estado_filtro,
    })

# def detalleTarea(request, tarea_id):
    # usuario_id = request.session.get('usuario_id')
    # if not usuario_id:
        # return redirect('login')
# 
    # tarea = get_object_or_404(Tareas, id=tarea_id, usuario_id=usuario_id)
# 
    # if request.method == 'POST':
        # texto_comentario = request.POST.get('texto', '').strip()
        # imagen_comentario = request.FILES.get('imagen')
        # 
        # if texto_comentario or imagen_comentario:
            # usuario_instancia = Usuario.objects.get(id=usuario_id)
            # Comentario.objects.create(
                # texto=texto_comentario,
                # imagen=imagen_comentario,
                # tarea=tarea,
                # usuario=usuario_instancia
            # )
            # return redirect('detalleTarea', tarea_id=tarea.id)
# 
    # comentarios = tarea.comentarios.all().order_by('-fecha_creacion')
# 
    # return render(request, 'detalleTarea.html', {
        # 'tarea': tarea,
        # 'comentarios': comentarios
    # })

@login_required
def detalleTarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id, usuario=request.user)

    if request.method == 'POST':
        texto_comentario = request.POST.get('texto', '').strip()
        imagen_comentario = request.FILES.get('imagen')
        
        if texto_comentario or imagen_comentario:
            Comentario.objects.create(
                texto=texto_comentario,
                imagen=imagen_comentario,
                tarea=tarea,
                usuario=request.user 
            )
            return redirect('detalleTarea', tarea_id=tarea.id)

    comentarios = tarea.comentarios.all().order_by('-fecha_creacion')

    return render(request, 'detalleTarea.html', {
        'tarea': tarea,
        'comentarios': comentarios
    })

@login_required
def eliminarComentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    tarea_id = comentario.tarea.id
    comentario.delete()
    return redirect('detalleTarea', tarea_id=tarea_id)

@login_required
def editarComentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    #usuario_id = request.session.get('usuario_id')
    
    # Comprobar permisos del usuario
    #if usuario_id is None or int(comentario.usuario.id) != int(usuario_id):
    #    return redirect('detalleTarea', tarea_id=comentario.tarea.id)

    if request.method == 'POST':
        form = EditarComentarioForm(request.POST, request.FILES, instance=comentario)
        if form.is_valid():
            form.save()  
            return redirect('detalleTarea', tarea_id=comentario.tarea.id)
    else:
        form = EditarComentarioForm(instance=comentario)

    return render(request, 'editarComentario.html', {
        'form': form,
        'comentario': comentario
    })

@login_required
def duplicarTarea(request, tarea_id):
    if request.method != 'POST':
        return redirect('tareas')

    es_admin = request.user.perfil.rol == Perfil.Rol.ADMINISTRADOR
    es_jefe = request.user.perfil.rol == Perfil.Rol.JEFE_EQUIPO
    
    if not (es_admin or es_jefe or request.user.is_superuser):
        messages.error(request, "No tienes permisos para crear usuarios.")
        return redirect('usuarios')  

    tarea_original = get_object_or_404(Tareas, id=tarea_id, usuario=request.user)

    # 1. Guardar referencia a la imagen antes de clonar la instancia
    imagen_original = tarea_original.imagen if hasattr(tarea_original, 'imagen') and tarea_original.imagen else None

    # 2. Al poner pk e id en None django tratara al objeto como un registro nuevo
    tarea_copia = tarea_original
    tarea_copia.pk = None
    tarea_copia.id = None
    
    
    tarea_copia.titulo = tarea_original.titulo + " (Copia)"
    
    if imagen_original:
        nombre_archivo = imagen_original.name.split('/')[-1] #Corta el texto por cada barra y te da el ultimo corte que ha hecho(Empieza a contar desde el final)
        
        
        tarea_copia.imagen.save(
            "copia_" + nombre_archivo, 
            ContentFile(imagen_original.read()), 
            save=False
        )

    tarea_copia.save()

    return redirect('tareas')

@login_required
def cambiarEstadoCronometro(request, tarea_id):
    if request.method == 'POST':
        tarea = get_object_or_404(Tareas, id=tarea_id)
        
        # si ya estaba comenzado: Calculamos la diferencia y detenemos
        if tarea.inicio_trabajo:
            ahora = timezone.now()
            diferencia = ahora - tarea.inicio_trabajo
            
            
            horas_transcurridas = Decimal(str(diferencia.total_seconds() / 3600))
            
            # sumamos al tiempo trabajado y reseteamos el inicio
            tarea.tiempo_trabajado += horas_transcurridas
            tarea.inicio_trabajo = None
            tarea.save()
            
        # si no habia empezado guardamos la hora actual
        else:
            tarea.inicio_trabajo = timezone.now()
            tarea.save()

    return redirect('tareas')


def crearPataton(request):
    if request.method == 'POST':
        form = CrearNuevoPataton(request.POST)
        if form.is_valid():
            tarea = form.save() 
            return redirect('pataton') 
    else:
        form = CrearNuevoPataton() 

    
    return render(request, 'crearPatatones.html', {
        'form': form
    })

def eliminarPataton(request, id):
    pataton = get_object_or_404(Pataton, id=id)
    pataton.delete()
    return redirect('pataton')

def editarPataton(request, id):
    pataton = get_object_or_404(Pataton, id=id)

    if request.method == 'POST':
        
        form = EditarPataton(request.POST, instance=pataton)
        if form.is_valid():
            form.save() 
            return redirect('pataton')
    else:
        # Petición GET: le pasamos 'instance=tarea' para que cargue los datos actuales
        form = EditarPataton(instance=pataton)

    return render(request, 'editarPataton.html', {
        'form': form,
        'pataton': pataton
    })


