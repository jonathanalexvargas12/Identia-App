# config/decorators.py
from functools import wraps
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import redirect


def developer_required(view_func):
    """Decorador para requerir rol de desarrollador"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': 'Autenticación requerida',
                    'message': 'Debe iniciar sesión para acceder a esta función'
                }, status=401)
            return redirect('usuarios:login')
        
        # Verificar si es desarrollador
        if not is_developer(request):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': 'Acceso restringido',
                    'message': 'Solo los usuarios desarrolladores pueden acceder a esta función'
                }, status=403)
            return HttpResponseForbidden('<h1>403 - Acceso Restringido</h1><p>Solo los usuarios desarrolladores pueden acceder a esta sección.</p>')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def is_developer(request):
    """Verifica si el usuario tiene rol de desarrollador"""
    # Verificar en sesión
    rol = request.session.get('empleado_rol', '').lower()
    if 'desarrollador' in rol or 'developer' in rol or 'desarrollo' in rol:
        return True
    
    # Verificar si es superuser
    if request.user.is_superuser:
        return True
    
    # Verificar en grupos
    if request.user.groups.filter(name__icontains='desarrollador').exists():
        return True
    
    # Verificar si tiene permisos de staff
    if request.user.is_staff:
        return True
    
    return False


def api_developer_required(view_func):
    """Decorador específico para APIs de desarrollo"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'Autenticación requerida'
            }, status=401)
        
        if not is_developer(request):
            return JsonResponse({
                'error': 'Acceso restringido',
                'message': 'Solo desarrolladores'
            }, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*roles):
    """
    Decorador para requerir un rol específico.
    Uso: @role_required('Administrador', 'Seguridad')
    
    Los roles válidos son: 'Administrador', 'Seguridad'
    El superusuario siempre tiene acceso.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('usuarios:login')
            
            # Superuser siempre tiene acceso
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Verificar rol desde la sesión
            user_rol = request.session.get('empleado_rol', '')
            if user_rol in roles:
                return view_func(request, *args, **kwargs)
            
            # Sin acceso
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': 'Acceso restringido',
                    'message': 'No tienes permisos para realizar esta acción'
                }, status=403)
            
            return HttpResponseForbidden(
                '<h1>403 - Acceso Restringido</h1>'
                '<p>No tienes permisos para acceder a esta sección.</p>'
            )
        return wrapper
    return decorator
