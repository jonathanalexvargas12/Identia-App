"""
Utilidades para el sistema de auditoría/bitácora.
Registra todas las acciones importantes del sistema.
"""
import logging
import requests
import socket
import os
import subprocess
import threading
from django.db import connection
from django.conf import settings
from datetime import datetime
import json

logger = logging.getLogger(__name__)

# Cache para la IP pública (para no consultar en cada request)
_public_ip_cache = None
_public_ip_timestamp = None
CACHE_DURATION = 300  # 5 minutos en segundos

# ==============================================
# FUNCIÓN PARA REPRODUCIR SONIDO (MEJORADA CON PYGAME)
# ==============================================
def reproducir_sonido_notificacion():
    """
    Reproduce el sonido de notificación usando pygame (mejor calidad).
    Se ejecuta en un hilo separado para no bloquear la aplicación.
    """
    def _reproducir():
        try:
            # Intentar importar pygame
            try:
                import pygame
            except ImportError:
                logger.warning("⚠️ pygame no está instalado. Instálalo con: pip install pygame")
                return
            
            sonido_path = os.path.join(settings.MEDIA_ROOT, 'notificacion.mp3')
            
            # Verificar que el archivo existe
            if not os.path.exists(sonido_path):
                logger.warning(f"⚠️ Archivo de sonido no encontrado: {sonido_path}")
                return
            
            # Inicializar pygame mixer con mejor configuración
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            
            # Cargar y reproducir
            pygame.mixer.music.load(sonido_path)
            pygame.mixer.music.set_volume(0.5)  # Volumen al 50% para evitar distorsión
            pygame.mixer.music.play()
            
            # Esperar a que termine sin bloquear demasiado
            # (timeout de 2 segundos máximo para no detener la app)
            tiempo_espera = 0
            while pygame.mixer.music.get_busy() and tiempo_espera < 20:  # Máximo 2 segundos
                pygame.time.wait(100)
                tiempo_espera += 1
                
        except Exception as e:
            logger.error(f"Error reproduciendo sonido con pygame: {str(e)}")
    
    # Ejecutar en un hilo separado para no bloquear
    thread = threading.Thread(target=_reproducir)
    thread.daemon = True
    thread.start()


def get_public_ip():
    """
    Obtiene la IP pública real del servidor/cliente consultando servicios externos.
    Esta función se usa como fallback cuando no se puede obtener la IP del cliente.
    """
    global _public_ip_cache, _public_ip_timestamp
    
    # Verificar si tenemos una IP en caché y sigue siendo válida
    from time import time
    ahora = time()
    if _public_ip_cache and _public_ip_timestamp and (ahora - _public_ip_timestamp) < CACHE_DURATION:
        logger.debug(f"Usando IP pública desde caché: {_public_ip_cache}")
        return _public_ip_cache
    
    # Lista de servicios para obtener IP pública (por si alguno falla)
    servicios = [
        'https://api.ipify.org',
        'https://api.myip.com',
        'https://httpbin.org/ip',
        'https://jsonip.com',
        'https://ident.me'
    ]
    
    for servicio in servicios:
        try:
            logger.debug(f"Consultando IP pública a: {servicio}")
            response = requests.get(servicio, timeout=3)
            
            if response.status_code == 200:
                # Diferentes servicios devuelven diferentes formatos
                if 'ipify' in servicio:
                    ip = response.text.strip()
                elif 'myip' in servicio:
                    data = response.json()
                    ip = data.get('ip', '')
                elif 'httpbin' in servicio:
                    data = response.json()
                    ip = data.get('origin', '').split(',')[0].strip()
                elif 'jsonip' in servicio:
                    data = response.json()
                    ip = data.get('ip', '')
                elif 'ident' in servicio:
                    ip = response.text.strip()
                else:
                    ip = response.text.strip()
                
                # Validar que sea una IP válida
                if ip and validar_ip(ip):
                    _public_ip_cache = ip
                    _public_ip_timestamp = ahora
                    logger.info(f"IP pública obtenida: {ip} (desde {servicio})")
                    return ip
                    
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error consultando {servicio}: {str(e)}")
            continue
        except Exception as e:
            logger.warning(f"Error inesperado con {servicio}: {str(e)}")
            continue
    
    # Si todos los servicios fallan, obtener IP local no loopback
    ip_local = get_local_ip()
    logger.warning(f"No se pudo obtener IP pública. Usando IP local: {ip_local}")
    return ip_local


def get_local_ip():
    """
    Obtiene la IP local no loopback (para usar como fallback).
    """
    try:
        # Crear conexión temporal para obtener IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()[0]
        s.close()
        return ip_local
    except Exception as e:
        logger.error(f"Error obteniendo IP local: {str(e)}")
        return "0.0.0.0"


def validar_ip(ip):
    """
    Valida que una cadena sea una IP válida (IPv4 o IPv6).
    """
    import re
    
    # Patrón para IPv4
    patron_ipv4 = r'^(\d{1,3}\.){3}\d{1,3}$'
    
    # Validar IPv4
    if re.match(patron_ipv4, ip):
        partes = ip.split('.')
        for parte in partes:
            if int(parte) > 255:
                return False
        return True
    
    # Validar IPv6 (simplificado)
    patron_ipv6 = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
    if re.match(patron_ipv6, ip):
        return True
    
    return False


def get_client_ip(request):
    """
    Obtiene la dirección IP REAL del cliente, incluso detrás de proxies.
    Ahora intenta obtener la IP pública real en lugar de localhost.
    """
    # Lista de headers que pueden contener la IP real
    ip_headers = [
        'HTTP_X_FORWARDED_FOR',
        'X_FORWARDED_FOR',
        'HTTP_CLIENT_IP',
        'HTTP_X_REAL_IP',
        'X_REAL_IP',
        'HTTP_X_FORWARDED',
        'X_FORWARDED',
        'HTTP_FORWARDED_FOR',
        'FORWARDED_FOR',
        'HTTP_X_CLUSTER_CLIENT_IP',
        'HTTP_CF_CONNECTING_IP',  # Cloudflare
        'CF_CONNECTING_IP',       # Cloudflare
        'HTTP_INCAP_CLIENT_IP',    # Incapsula
        'X_CLUSTER_CLIENT_IP',
    ]
    
    # 1. Primero intentar obtener de los headers (para cuando está detrás de proxy)
    for header in ip_headers:
        ip_list = request.META.get(header, '')
        if ip_list:
            # Puede venir como lista separada por comas
            ip = ip_list.split(',')[0].strip()
            if ip and validar_ip(ip):
                logger.debug(f"IP obtenida de header {header}: {ip}")
                return ip
    
    # 2. Si no hay headers, usar REMOTE_ADDR
    remote_addr = request.META.get('REMOTE_ADDR', '')
    if remote_addr and remote_addr != '127.0.0.1' and remote_addr != '::1':
        logger.debug(f"IP obtenida de REMOTE_ADDR: {remote_addr}")
        return remote_addr
    
    # 3. Si estamos en localhost (127.0.0.1), intentar obtener IP pública
    if remote_addr in ['127.0.0.1', '::1', '']:
        logger.info("Cliente en localhost, consultando IP pública real...")
        public_ip = get_public_ip()
        if public_ip:
            return public_ip
    
    # 4. Fallback final
    logger.warning("No se pudo determinar IP del cliente")
    return "0.0.0.0"


def registrar_incidente(request, usuario_id, novedad, detalles=None):
    """
    Registra un incidente en la bitácora.
    
    Args:
        request: Objeto request de Django (para obtener IP)
        usuario_id: ID del usuario que realiza la acción
        novedad: Título o resumen del evento (VARCHAR(100))
        detalles: Descripción amplia del suceso (TEXT)
    
    Returns:
        bool: True si se registró correctamente
    """
    try:
        ip = get_client_ip(request)
        ahora = datetime.now()
        
        # Limitar longitud de novedad a 100 caracteres
        if novedad and len(novedad) > 100:
            novedad = novedad[:97] + "..."
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO bitacora_incidentes 
                (novedad, detalles, hora, fecha, ip)
                VALUES (%s, %s, %s, %s, %s)
            """, [novedad, detalles, ahora.time(), ahora.date(), ip])
            connection.commit()
            
            # ==============================================
            # REPRODUCIR SONIDO DE NOTIFICACIÓN (CON PYGAME)
            # ==============================================
            # Solo reproducir para tipos relevantes de notificaciones
            tipos_con_sonido = ['login', 'logout', 'agregar', 'editar', 'eliminar', 'activar', 'desactivar']
            
            # Determinar el tipo de evento
            try:
                from .views import determinar_tipo_evento
                tipo = determinar_tipo_evento(novedad)
                logger.info(f"Tipo de evento determinado: {tipo} para novedad: {novedad}")
                
                if tipo in tipos_con_sonido:
                    # Ejecutar en hilo separado para no bloquear
                    threading.Thread(target=reproducir_sonido_notificacion, daemon=True).start()
            except ImportError as e:
                # Si no se puede importar, reproducir para todos los incidentes
                logger.error(f"Error importando determinar_tipo_evento: {e}")
                threading.Thread(target=reproducir_sonido_notificacion, daemon=True).start()
        
        logger.info(f"Incidente registrado: {novedad} - IP: {ip}")
        return True
    
    except Exception as e:
        logger.error(f"Error registrando incidente en bitácora: {str(e)}")
        return False


def registrar_acceso(request, usuario_id, tipo_acceso):
    """
    Registra accesos al sistema (login/logout).
    """
    from django.db import connection
    
    # Obtener información del usuario
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT nombres, apellidos, cedula 
                FROM usuarios WHERE id_pk = %s
            """, [usuario_id])
            user_data = cursor.fetchone()
            if user_data:
                nombre_completo = f"{user_data[0]} {user_data[1]}".strip()
                cedula = user_data[2]
                usuario_info = f"{nombre_completo} (C.I: {cedula})"
            else:
                usuario_info = f"ID Usuario: {usuario_id}"
    except:
        usuario_info = f"ID Usuario: {usuario_id}"
    
    novedad = f"{'INICIO' if tipo_acceso == 'login' else 'CIERRE'} DE SESIÓN"
    detalles = f"El usuario {usuario_info} {'inició' if tipo_acceso == 'login' else 'cerró'} sesión en el sistema"
    
    return registrar_incidente(request, usuario_id, novedad, detalles)


def registrar_crud_action(request, usuario_id, accion, modulo, objeto_id=None, objeto_descripcion=None):
    """
    Registra acciones CRUD en los diferentes módulos.
    
    Args:
        request: Objeto request de Django
        usuario_id: ID del usuario
        accion: AGREGAR, EDITAR, ELIMINAR, ACTIVAR, DESACTIVAR, etc.
        modulo: Nombre del módulo (ej: "TIPOS_PERSONAL", "HORARIOS", "USUARIOS")
        objeto_id: ID del objeto afectado (opcional)
        objeto_descripcion: Descripción del objeto (opcional)
    """
    from django.db import connection
    
    # Mapeo de acciones a mensajes más legibles
    acciones_legibles = {
        'AGREGAR': 'AGREGÓ',
        'EDITAR': 'EDITÓ',
        'ELIMINAR': 'ELIMINÓ',
        'ACTIVAR': 'ACTIVÓ',
        'DESACTIVAR': 'DESACTIVÓ',
        'ACTUALIZAR': 'ACTUALIZÓ',
        'AJUSTAR': 'AJUSTÓ',
        'DETECTAR': 'DETECTÓ',
    }
    
    verbo = acciones_legibles.get(accion, accion)
    
    # Obtener información del usuario
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT nombres, apellidos, cedula 
                FROM usuarios WHERE id_pk = %s
            """, [usuario_id])
            user_data = cursor.fetchone()
            if user_data:
                nombre_completo = f"{user_data[0]} {user_data[1]}".strip()
                cedula = user_data[2]
                usuario_info = f"{nombre_completo} (C.I: {cedula})"
            else:
                usuario_info = f"Usuario ID: {usuario_id}"
    except:
        usuario_info = f"Usuario ID: {usuario_id}"
    
    # Construir novedad (título corto - VARCHAR(100))
    if objeto_descripcion:
        novedad = f"{verbo} en {modulo}"
        if len(novedad) > 100:
            novedad = novedad[:97] + "..."
    else:
        novedad = f"{verbo} en {modulo}"
    
    # Construir detalles completos
    if objeto_descripcion and objeto_id:
        detalles = f"El usuario {usuario_info} {verbo.lower()} {objeto_descripcion} (ID: {objeto_id}) en el módulo {modulo}"
    elif objeto_id:
        detalles = f"El usuario {usuario_info} {verbo.lower()} registro con ID {objeto_id} en el módulo {modulo}"
    elif objeto_descripcion:
        detalles = f"El usuario {usuario_info} {verbo.lower()} {objeto_descripcion} en el módulo {modulo}"
    else:
        detalles = f"El usuario {usuario_info} realizó acción: {accion} en el módulo {modulo}"
    
    return registrar_incidente(request, usuario_id, novedad, detalles)


def registrar_evento_sistema(request, usuario_id, titulo, descripcion):
    """
    Registra un evento personalizado en la bitácora.
    """
    return registrar_incidente(request, usuario_id, titulo, descripcion)


# Opcional: Función para obtener geolocalización aproximada por IP
def get_geolocation(ip):
    """
    Obtiene ubicación aproximada de una IP (opcional, requiere API key).
    """
    if ip in ['127.0.0.1', '::1', '0.0.0.0', 'localhost']:
        return None
    
    try:
        # Usar ip-api.com (gratuito, sin API key)
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return f"{data.get('city', '')}, {data.get('country', '')}"
    except:
        pass
    
    return None