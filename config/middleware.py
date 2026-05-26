# config/middleware.py
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
import re


class SecurityHeadersMiddleware:
    """Middleware para añadir cabeceras de seguridad"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Cabeceras de seguridad
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        
        # Prevenir que se detecte el tipo de servidor
        response['Server'] = 'WebServer'
        
        return response


class DeveloperOnlyAccessMiddleware:
    """Middleware para restringir acceso a herramientas de desarrollo"""
    
    # Rutas que solo pueden acceder desarrolladores
    DEVELOPER_ONLY_PATHS = [
        r'^/admin/',
        r'^/api/debug/',
        r'^/dev/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        path = request.path
        
        # Verificar si es una ruta de desarrollo
        for pattern in self.DEVELOPER_ONLY_PATHS:
            if re.match(pattern, path):
                # Verificar si el usuario es desarrollador
                if not self.is_developer(request):
                    # Si no es desarrollador, redirigir o denegar
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'error': 'Acceso restringido',
                            'message': 'Esta sección es solo para desarrolladores'
                        }, status=403)
                    return redirect('usuarios:home_principal')
        
        return self.get_response(request)
    
    def is_developer(self, request):
        """Verifica si el usuario tiene rol de desarrollador"""
        if not request.user.is_authenticated:
            return False
        
        # Verificar en sesión
        rol = request.session.get('empleado_rol', '').lower()
        if 'desarrollador' in rol or 'developer' in rol or 'admin' in rol:
            return True
        
        # Verificar en usuario Django
        if request.user.is_superuser:
            return True
        
        # Verificar en grupo
        if request.user.groups.filter(name__icontains='desarrollador').exists():
            return True
        
        return False


class DisableSessionCookiesMiddleware:
    """Middleware para prevenir robo de cookies en XSS"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # HttpOnly ya está configurado por defecto en Django
        # SameSite attribute
        if request.session.session_key:
            response['Set-Cookie'] = (
                f'sessionid={request.session.session_key}; '
                'HttpOnly; '
                'Secure; '
                'SameSite=Strict; '
                'Path=/'
            )
        
        return response


class RequestValidationMiddleware:
    """Middleware para validar y sanitizar requests"""
    
    # Headers que indican herramientas de desarrollo
    SUSPICIOUS_HEADERS = [
        'DevToolsServerUrl',
        'Chrome-Transport-State',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Verificar headers sospechosos
        for header in self.SUSPICIOUS_HEADERS:
            if request.META.get(header):
                return JsonResponse({
                    'error': 'Acceso denegado',
                    'message': 'Herramientas de desarrollo no permitidas'
                }, status=403)
        
        # Verificar User-Agent sospechoso
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        suspicious_agents = ['curl', 'wget', 'postman', 'insomnia', 'charles', 'fiddler']
        for agent in suspicious_agents:
            if agent in user_agent:
                # Solo denegar si no es usuario autenticado
                if not request.user.is_authenticated:
                    return JsonResponse({
                        'error': 'Acceso denegado',
                        'message': 'User agent no permitido'
                    }, status=403)
        
        return self.get_response(request)
