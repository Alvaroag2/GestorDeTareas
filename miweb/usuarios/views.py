from django.contrib import messages
from django.shortcuts import get_object_or_404, render , redirect
import json
from .models import Perfil, Usuario
from .forms import CrearNuevoUsuario
from .forms import EditarUsuario
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.middleware.csrf import get_token
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

# Create your views here.


def api_csrf(request):
    return JsonResponse({'csrf_token': get_token(request)})

@csrf_exempt  # 1. Permite procesar el login sin exigir la cookie previa
@ensure_csrf_cookie
def api_login(request):
    if request.method == 'GET':
        return JsonResponse({"detail": "CSRF cookie set"})
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            from django.contrib.auth.models import User
            user_obj = User.objects.filter(username=username).first()

            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
                if user is not None:
                    auth_login(request, user)

                    # Obtener el rol del Perfil
                    rol = getattr(getattr(user, 'perfil', None), 'rol', 'COMUN')

                    return JsonResponse({
                        "id": user.id,
                        "nombre": user.first_name or user.username,
                        "rol": rol
                    })

            return JsonResponse({"error": "Credenciales inválidas"}, status=401)
        except Exception as e:
            return JsonResponse({"error": "Petición no válida"}, status=400)

def api_sesion(request):
    if request.user.is_authenticated:
        rol = getattr(getattr(request.user, 'perfil', None), 'rol', 'COMUN')
        return JsonResponse({
            "id": request.user.id,
            "nombre": request.user.first_name or request.user.username,
            "email": request.user.email,
            "rol": rol
        })
    else:
        return JsonResponse({"error": "No hay sesión iniciada"}, status=401)


@require_POST
@csrf_exempt
def api_logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return JsonResponse({"mensaje": "Sesión cerrada correctamente"})
    return JsonResponse({"error": "No había sesión activa"}, status=400)


@ensure_csrf_cookie
def api_usuarios(request):
    # GET /api/usuarios/ -> Listar todos los usuarios
    if request.method == 'GET':
        usuarios_qs = User.objects.all().select_related('perfil')
        # 1. Obtenemos el parámetro 'rol' de la URL (?rol=COMUN)
        rol_filtro = request.GET.get('rol', None)

        # 2. Si viene el filtro 'rol', filtramos la consulta a través de la relación Perfil
        if rol_filtro:
            usuarios_qs = usuarios_qs.filter(perfil__rol=rol_filtro)
        data = []
        for u in usuarios_qs:
            rol = u.perfil.rol if hasattr(u, 'perfil') and u.perfil else 'COMUN'
            data.append({
                "id": u.id,
                "nombre": u.username,
                "email": u.email,
                "rol": rol
            })
        return JsonResponse(data, safe=False, status=200)

    # POST /api/usuarios/ -> Crear un usuario
    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            nombre = body.get('username', '')
            email = body.get('email')
            password = body.get('password')
            rol = body.get('rol', 'COMUN')

            
            nuevo_usuario = User.objects.create_user(
                username=nombre,
                email=email,
                password=password,
            )

            Perfil.objects.create(
                usuario=nuevo_usuario,
                rol=rol
            )

            return JsonResponse({
                "id": nuevo_usuario.id,
                "nombre": nuevo_usuario.username,
                "email": nuevo_usuario.email,
                "rol": rol
            }, status=201)
        except Exception as e:
            
            print("❌ ERROR EN POST /api/usuarios/:", str(e))
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

    

@ensure_csrf_cookie
def api_usuario_detalle(request, id):
    usuario = get_object_or_404(User, id=id)

    # GET /api/usuarios/<id>/ -> Obtener usuario por ID
    if request.method == 'GET':
        rol = usuario.perfil.rol if hasattr(usuario, 'perfil') and usuario.perfil else 'COMUN'
        return JsonResponse({
            "id": usuario.id,
            "nombre": usuario.first_name or usuario.username,
            "email": usuario.email,
            "rol": rol
        }, status=200)


    elif request.method == 'PUT':
        try:
            body = json.loads(request.body)
            usuario.username = body.get('nombre', usuario.username)
            usuario.email = body.get('email', usuario.email)
            usuario.save()

            if hasattr(usuario, 'perfil') and usuario.perfil:
                usuario.perfil.rol = body.get('rol', usuario.perfil.rol)
                usuario.perfil.save()
            else:
                Perfil.objects.create(usuario=usuario, rol=body.get('rol', 'COMUN'))

            rol_actualizado = usuario.perfil.rol

            return JsonResponse({
                "id": usuario.id,
                "nombre": usuario.username,
                "email": usuario.email,
                "rol": rol_actualizado
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": "Error al actualizar el usuario"}, status=400)

   

    # DELETE /api/usuarios/<id>/ -> Borrar usuario
    elif request.method == 'DELETE':
        usuario.delete()
        return HttpResponse(status=204)

    return JsonResponse({"error": "Método no permitido"}, status=405)