"""
Utilidades para el procesamiento facial.
"""
import numpy as np
import cv2
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def preprocess_image(image_data, target_size=(640, 640)):
    """
    Preprocesa una imagen para el modelo facial.
    
    Args:
        image_data: Bytes de la imagen o array numpy
        target_size: Tamaño objetivo (ancho, alto)
    
    Returns:
        np.array: Imagen preprocesada
    """
    try:
        # Si son bytes, decodificar
        if isinstance(image_data, bytes):
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        else:
            img = image_data
        
        if img is None:
            raise ValueError("No se pudo decodificar la imagen")
        
        # Convertir BGR a RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Redimensionar manteniendo aspect ratio
        h, w = img_rgb.shape[:2]
        target_w, target_h = target_size
        
        # Calcular nuevo tamaño manteniendo proporción
        scale = min(target_w / w, target_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        img_resized = cv2.resize(img_rgb, (new_w, new_h))
        
        # Crear imagen con padding si es necesario
        delta_w = target_w - new_w
        delta_h = target_h - new_h
        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)
        
        img_padded = cv2.copyMakeBorder(
            img_resized, top, bottom, left, right,
            cv2.BORDER_CONSTANT, value=[0, 0, 0]
        )
        
        return img_padded
    
    except Exception as e:
        logger.error(f"Error en preprocesamiento: {str(e)}")
        raise

def calculate_similarity(embedding1, embedding2):
    """
    Calcula la similitud coseno entre dos embeddings.
    
    Args:
        embedding1: Primer vector facial
        embedding2: Segundo vector facial
    
    Returns:
        float: Similitud (0-1)
    """
    # Normalizar vectores
    emb1_norm = embedding1 / np.linalg.norm(embedding1)
    emb2_norm = embedding2 / np.linalg.norm(embedding2)
    
    # Calcular similitud coseno
    similarity = np.dot(emb1_norm, emb2_norm)
    
    return float(similarity)

def validate_face_quality(face, min_size=100, min_confidence=0.5):
    """
    Valida la calidad de un rostro detectado.
    
    Args:
        face: Objeto de rostro de InsightFace
        min_size: Tamaño mínimo del rostro en píxeles
        min_confidence: Confianza mínima de detección
    
    Returns:
        tuple: (bool_valido, dict_errores)
    """
    errors = []
    
    # Validar confianza
    if face.det_score < min_confidence:
        errors.append(f"Confianza baja: {face.det_score:.2f}")
    
    # Validar tamaño
    bbox = face.bbox.astype(int)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    
    if width < min_size or height < min_size:
        errors.append(f"Rostro muy pequeño: {width}x{height}")
    
    # Validar puntos de referencia
    if not hasattr(face, 'kps') or face.kps is None:
        errors.append("No se detectaron puntos faciales")
    
    # Validar que esté centrado
    if width > 0 and height > 0:
        aspect_ratio = width / height
        if aspect_ratio < 0.7 or aspect_ratio > 1.3:
            errors.append(f"Proporción inusual: {aspect_ratio:.2f}")
    
    is_valid = len(errors) == 0
    
    return is_valid, {
        'is_valid': is_valid,
        'errors': errors,
        'bbox_size': (width, height),
        'confidence': float(face.det_score),
        'has_landmarks': hasattr(face, 'kps') and face.kps is not None
    }