"""
Utilidades para el módulo de reconocimiento facial.
Maneja la reproducción de sonidos para diferentes eventos.
"""
import os
import threading
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# ==============================================
# MAPEO DE SONIDOS POR TIPO DE EVENTO
# ==============================================
SONIDOS = {
    # Acceso denegado
    'denegado_no_rostro': 'denegado_no_rostro.mp3',
    'denegado_inactivo': 'denegado_inactivo.mp3',
    'denegado_sin_facial': 'denegado_sin_facial.mp3',
    'denegado_suspendido': 'denegado_suspendido.mp3',
    
    # Acceso permitido
    'permitido_activo': 'permitido_activo.mp3',
    'permitido_vacaciones': 'permitido_vacaciones.mp3',
}

def reproducir_sonido(tipo_evento, volumen=0.5):
    """
    Reproduce un sonido específico según el tipo de evento.
    
    Args:
        tipo_evento: Clave del sonido a reproducir (ej: 'permitido_activo')
        volumen: Volumen de reproducción (0.0 a 1.0)
    """
    def _reproducir():
        try:
            # Intentar importar pygame
            try:
                import pygame
            except ImportError:
                logger.warning("⚠️ pygame no está instalado. Instálalo con: pip install pygame")
                return
            
            # Obtener nombre del archivo
            nombre_archivo = SONIDOS.get(tipo_evento)
            if not nombre_archivo:
                logger.warning(f"⚠️ No hay sonido definido para el evento: {tipo_evento}")
                return
            
            # Construir ruta completa
            sonido_path = os.path.join(settings.MEDIA_ROOT, nombre_archivo)
            
            # Verificar que el archivo existe
            if not os.path.exists(sonido_path):
                logger.warning(f"⚠️ Archivo de sonido no encontrado: {sonido_path}")
                return
            
            # Inicializar pygame mixer con configuración óptima
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            
            # Cargar y reproducir
            pygame.mixer.music.load(sonido_path)
            pygame.mixer.music.set_volume(volumen)
            pygame.mixer.music.play()
            
            # Esperar a que termine sin bloquear demasiado (máx 3 segundos)
            tiempo_espera = 0
            while pygame.mixer.music.get_busy() and tiempo_espera < 30:  # 3 segundos
                pygame.time.wait(100)
                tiempo_espera += 1
                
        except Exception as e:
            logger.error(f"Error reproduciendo sonido {tipo_evento}: {str(e)}")
    
    # Ejecutar en un hilo separado para no bloquear
    thread = threading.Thread(target=_reproducir)
    thread.daemon = True
    thread.start()


def reproducir_segun_estado(estado_normalizado, hay_coincidencia=True, no_hay_coincidencia=True, tipo_acceso=None):
    """
    Reproduce el sonido apropiado según el estado del usuario y el resultado.
    
    Args:
        estado_normalizado: Estado del usuario ('activo', 'inactivo', etc.)
        hay_coincidencia: Si no se encontró un rostro en la BD
        no_hay_coincidencia: Si se encontró un rostro pero no coincide con ningún registro
        tipo_acceso: Tipo específico de acceso (para casos especiales)
    """
    if not hay_coincidencia:
        # No se encontró rostro en BD
        reproducir_sonido('denegado_no_rostro')
        return
    
    if not no_hay_coincidencia:
        # Hay un rostro pero no coincide con ningún registro
        reproducir_sonido('denegado_sin_facial')
        return
    
    # Según el estado normalizado
    if estado_normalizado == 'activo':
        reproducir_sonido('permitido_activo')
    elif estado_normalizado == 'inactivo':
        reproducir_sonido('denegado_inactivo')
    elif estado_normalizado == 'vacaciones':
        reproducir_sonido('permitido_vacaciones')
    elif estado_normalizado == 'suspendido':
        reproducir_sonido('denegado_suspendido')
    else:
        # Caso por defecto (no debería ocurrir)
        logger.warning(f"Estado no reconocido para sonido: {estado_normalizado}")


def reproducir_sin_rostro_detectado():
    """Reproduce sonido cuando no se detecta ningún rostro en la imagen."""
    reproducir_sonido('denegado_no_rostro')