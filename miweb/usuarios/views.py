from django.contrib import messages
from django.shortcuts import get_object_or_404, render , redirect
from .models import Perfil, Usuario
from .forms import CrearNuevoUsuario
from .forms import EditarUsuario
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
# def usuarios(request):
#    usuario = Usuario.objects.all()
#    return render(request,'usuarios.html',{
    #    "usuario" : usuario
#    })

@login_required
def usuarios(request):
    usuario = User.objects.all() 
    return render(request, 'usuarios.html', {
        "usuario": usuario
    })

# def crearUsuarios(request):
    # if request.method == 'POST':
        # form = CrearNuevoUsuario(request.POST)
        # if form.is_valid():
            # usuario = form.save() 
            # return redirect('usuarios') 
    # else:
        # form = CrearNuevoUsuario() #Lo crea vacio
# 
    # 
    # return render(request, 'crearUsuarios.html', {
        # 'form': form
    # })

@login_required
def crearUsuarios(request):
    es_admin = request.user.perfil.rol == Perfil.Rol.ADMINISTRADOR
    es_jefe = request.user.perfil.rol == Perfil.Rol.JEFE_EQUIPO

    if not (es_admin or es_jefe or request.user.is_superuser):
        messages.error(request, "No tienes permisos para crear usuarios.")
        return redirect('usuarios')  

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save() 
            rol_elegido = request.POST.get('rol')

            Perfil.objects.create(
                usuario=nuevo_usuario,
                rol=rol_elegido
            )
            return redirect('usuarios') 
    else:
        form = UserCreationForm()

    return render(request, 'crearUsuarios.html', {
        'form': form
    })

# def eliminarUsuario(request, id):
    # usuario = get_object_or_404(Usuario, id=id)
    # usuario.delete()
    # return redirect('usuarios')

@login_required
def eliminarUsuario(request, id):
    es_admin = request.user.perfil.rol == Perfil.Rol.ADMINISTRADOR
    es_jefe = request.user.perfil.rol == Perfil.Rol.JEFE_EQUIPO
    
    if not (es_admin or es_jefe or request.user.is_superuser):
        messages.error(request, "No tienes permisos para crear usuarios.")
        return redirect('usuarios')  
    usuario = get_object_or_404(User, id=id) 
    usuario.delete()
    return redirect('usuarios')

# def editarUsuario(request, id):
    # usuario = get_object_or_404(Usuario, id=id)
# 
    # if request.method == 'POST':
        # 
        # form = EditarUsuario(request.POST, instance=usuario)
        # if form.is_valid():
            # form.save() 
            # return redirect('usuarios')
    # else:
        #Petición GET: le pasamos 'instance=tarea' para que cargue los datos actuales
        # form = EditarUsuario(instance=usuario)
# 
    # return render(request, 'editarTarea.html', {
        # 'form': form,
        # 'usuario': usuario
    # })

@login_required
def editarUsuario(request, id):
    usuario = get_object_or_404(User, id=id)  

    es_admin = request.user.perfil.rol == Perfil.Rol.ADMINISTRADOR
    es_jefe = request.user.perfil.rol == Perfil.Rol.JEFE_EQUIPO
    
    if not (es_admin or es_jefe or request.user.is_superuser):
        messages.error(request, "No tienes permisos para crear usuarios.")
        return redirect('usuarios')  

    if request.method == 'POST':
        
        form = UserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            
            nuevo_usuario = form.save() 
            rol_elegido = request.POST.get('rol')
            
            Perfil.objects.create(
            usuario=nuevo_usuario,
            rol=rol_elegido
            )
            return redirect('usuarios')
    else:
        form = UserChangeForm(instance=usuario)

    
    return render(request, 'editarUsuarios.html', {
        'form': form,
        'usuario': usuario
    })

# def login(request):
    # if request.method == 'POST':
        # correo_input = request.POST['correo']
        # clave_input = request.POST['contrasena']
# 
        # try:
            # 
            # usuario = Usuario.objects.get(correo=correo_input, contraseña=clave_input)
            # 
        #    
            # request.session['usuario_id'] = usuario.id #Crea una especie de cookie con la id del usuario para depsues usarlo en tareas
            # 
            # return redirect('tareas') 
            # 
        # except Usuario.DoesNotExist:
            # return render(request, 'login.html', {
                # 'error': 'El correo o la contraseña son incorrectos'
            # })
# 
    # 
    # return render(request, 'login.html')
# 
# def logout(request):
    #Borra todos los datos guardados en la sesión actual
    # request.session.flush()
    # return redirect('login')

#Login usando django auth
def login(request): 
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  #Django crea la sesión automáticamente
            return redirect('tareas')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

# 2. Tu nuevo Logout
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('login')
    return redirect('tareas')